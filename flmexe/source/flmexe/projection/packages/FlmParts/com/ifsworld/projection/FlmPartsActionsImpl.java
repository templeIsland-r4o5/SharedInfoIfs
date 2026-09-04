/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmFaultDeferral
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 */
package com.ifsworld.projection;

import com.fasterxml.jackson.databind.JsonNode;
import com.ifsworld.adcom.projection.util.AllowablePartRequest;
import com.ifsworld.adcom.projection.util.AllowablePartRequestTransformer;
import com.ifsworld.adcom.projection.util.AllowablePartResponseHandler;
import com.ifsworld.adcom.projection.util.AvExeTaskSensApi;
import com.ifsworld.adcom.projection.util.AvFaultApi;
import com.ifsworld.adcom.projection.util.EffectiveSensitivitiesResponseTransformer;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.Map;
import javax.json.JsonObject;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.logging.Level;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/*
 * Implementation class for all global actions defined in the FlmFaultDeferral projection model.
 */
@Stateless(name = "FlmPartsActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmPartsActionsImpl implements FlmPartsActions {

   private static final Logger LOGGER = LoggerFactory.getLogger(FlmPartsActionsImpl.class);

   private static final String MTX_EFFECTIVE_SENSITIVITY_SEARCH_API_PATH = "/amapi/materials/asset/aircraft/{aircraftAltId}/effectivesensitivitiesview";

   private static final String AURENA_AIRCRAFT_ALT_ID = "AircraftAltId";
   private static final String AURENA_CONFIG_SLOT_ALT_ID = "ConfigSlotAltId";
   private static final String AURENA_ETOPS_BOOL = "EtopsSignificant";
   private static final String AURENA_FAULT_ID = "FaultId";
   private static final String AURENA_TASK_PART_ID = "TaskPartId";

   @Override
   public Map<String, Object> getInterchangeableParts(Map<String, Object> parameters, Connection connection) {

      AllowablePartRequestTransformer allowablePartRequestTransformer = new AllowablePartRequestTransformer();
      JsonObject allowablePartRequestPayloadJson = allowablePartRequestTransformer.transformAllowablePartPayload(parameters);
      LOGGER.debug("Transformed Mtx cms Request json: {}", allowablePartRequestPayloadJson.toString());

      ApiRequest apiRequest = new ApiRequest(AllowablePartRequest.ALLOWABLE_PART_API_PATH, allowablePartRequestPayloadJson);
      ApiResponse allowablePartApiResponse = MaintenixApiProxy.post(apiRequest);
      LOGGER.debug("Mtx Allowable Part Api Response json: {}", allowablePartApiResponse.getResultJson());

      if (allowablePartApiResponse.getStatusCode() != 200) {
         LOGGER.error("Allowable Part API call failed. Status: {}, Response: {}", allowablePartApiResponse.getStatusCode(), allowablePartApiResponse.getResultJson());
         throw new ProjectionException("Allowable Part API call failed with status: " + allowablePartApiResponse.getStatusCode());
      }
      AllowablePartResponseHandler responseHandler = new AllowablePartResponseHandler();
      List<Map<String, String>> filteredParts = responseHandler.handleAllowablePartResponse(parameters, connection, allowablePartApiResponse.getResultJson());
      return null;
   }

   @Override
   public Map<String, Object> saveOverallTaskSensitivity(Map<String, Object> parameters, Connection connection) {
      String aircraftAltId = (String) parameters.get(AURENA_AIRCRAFT_ALT_ID);
      EffectiveSensitivitiesResponseTransformer effectiveSensitivitiesResponseTransformer = new EffectiveSensitivitiesResponseTransformer();
      LOGGER.debug("saveOverallTaskSensitivity Parameters {}", parameters);
      String apiPath = MTX_EFFECTIVE_SENSITIVITY_SEARCH_API_PATH.replace("{aircraftAltId}", aircraftAltId);

      try {
         ApiRequest apiRequest = new ApiRequest(apiPath, null);
         apiRequest = buildOverallTaskSensApiPath(apiRequest, parameters, connection);

         ApiResponse sensitivityApiResponse = MaintenixApiProxy.get(apiRequest);
         String sensitivityApiResponseJson = sensitivityApiResponse.getResultJson();
         int sensitivityApiResponseStatusCode = sensitivityApiResponse.getStatusCode();
         LOGGER.debug("Overall Task Sensitivity Api Response, status code: {}, response: {}", sensitivityApiResponseStatusCode, sensitivityApiResponseJson);

         EffectiveSensitivitiesResponseTransformer.handleHttpResponseStatus(sensitivityApiResponseStatusCode);
         effectiveSensitivitiesResponseTransformer.processOverallTaskSensResponse(connection, parameters, sensitivityApiResponseJson);

      } catch (SQLException ex) {
         LOGGER.error("SQL error occured ", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      } catch (Exception ex) {
         LOGGER.error("Error occured ", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      }
      return null;
   }

   public ApiRequest buildOverallTaskSensApiPath(ApiRequest apiRequest, Map<String, Object> parameters, Connection connection) throws SQLException {
      EffectiveSensitivitiesResponseTransformer effectiveSensitivitiesResponseTransformer = new EffectiveSensitivitiesResponseTransformer();
      AvFaultApi avFaultapi = new AvFaultApi(connection);
      int taskPartId = ((Number) parameters.get(AURENA_TASK_PART_ID)).intValue();
      int faultId = parameters.get(AURENA_FAULT_ID) != null ? ((Number) parameters.get(AURENA_FAULT_ID)).intValue() : 0;
      String configSlotAltId = (String) parameters.get(AURENA_CONFIG_SLOT_ALT_ID);
      boolean isEtops = Boolean.parseBoolean(effectiveSensitivitiesResponseTransformer.getParameterAsString(parameters, AURENA_ETOPS_BOOL));

      apiRequest.withParameter("is_etops", isEtops);
      if (faultId != 0) {
         apiRequest.withParameter("configuration_slot_id", configSlotAltId);
      }
      Set<String> partReqPartGroupAltIdsByTask = avFaultapi.getPartReqPartGroupAltIdsByTask(faultId, taskPartId);
      LOGGER.debug("Part Group Alt Ids: {}", partReqPartGroupAltIdsByTask);

      for (String id : partReqPartGroupAltIdsByTask) {
         apiRequest.withParameter("part_group_id", id);
      }

      return apiRequest;
   }
}
