/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmTaskDetailHandling
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 */
package com.ifsworld.projection;

import com.ifsworld.adcom.projection.util.FaultProjectionHelper;
import com.ifsworld.adcom.projection.util.FaultRequestTransformer;
import com.ifsworld.adcom.projection.util.FaultResponseTransformer;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.IfsCloudFlowHeader;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import com.ifsworld.mxcore.projection.api.ResponseUtils;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.Map;
import javax.json.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import javax.json.Json;
import javax.json.JsonArrayBuilder;
import javax.json.JsonObjectBuilder;

/*
 * Implementation class for all global actions defined in the FlmTaskDetailHandling projection model.
 */
@Stateless(name = "FlmTaskDetailHandlingActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmTaskDetailHandlingActionsImpl extends FlmTaskDetailHandlingActionsFragmentsWrapper implements FlmTaskDetailHandlingActions {

   private static final Logger LOGGER = LoggerFactory.getLogger(FlmTaskDetailHandlingActionsImpl.class);
   private static final String MTX_FAULT_API_PATH = "amapi/batch";
   private static final String MTX_EVALUATE_NON_ROUTINE_API_PATH = "maintenance/exec/fault/";
   
   private static final String EVALUATED = "evaluated";
   private static final String REQUEST = "request";
   private static final String METHOD = "method";
   private static final String PUT = "PUT";
   private static final String API_CALLS = "apiCalls";
   private static final String HEADERS = "headers";
   private static final String ACCEPT = "Accept";
   private static final String APPLICATION_VND_IFS_AMAPI_V_2_JSON = "application/vnd.ifs.amapi.v2+json";
   private static final String URL = "url";
   private static final String BODY = "body";
   private static final String CONTENT_TYPE = "Content-Type";

   @Override
   public Map<String, Object> faultProjectionService(Map<String, Object> parameters, Connection connection) {
      
      FaultProjectionHelper fault = new FaultProjectionHelper(connection);
      FaultResponseTransformer faultResponseTransformer = new FaultResponseTransformer(connection);
      FaultRequestTransformer faultRequestTransformer = new FaultRequestTransformer(connection);

      try {
         // Raise NonRoutine/LogBook fault in MM
         LOGGER.debug("FaultProjectionService FLM request param: {}", parameters.toString());
         fault.raiseFaultInMM(parameters);

         // Raise NonRoutine/LogBook fault in Mx
         JsonObject faultRequestPayloadJson = faultRequestTransformer.transformFaultPayload(parameters);
         LOGGER.debug("Transformed Mtx NonRoutine/LogBook fault Request json: {}", faultRequestPayloadJson.toString());

         ApiRequest apiRequest = new ApiRequest(MTX_FAULT_API_PATH, faultRequestPayloadJson);
         apiRequest.addHeader(IfsCloudFlowHeader.MEX_RAISE_FAULT);
         ApiResponse faultApiResponse = MaintenixApiProxy.post(apiRequest);
         LOGGER.debug("Mtx NonRoutine/LogBook fault Api Response status code: {} response json: {}", faultApiResponse.getStatusCode(), faultApiResponse.getResultJson());

         // Persist Mx Keys on MM entities
         String faultResponseJson = faultResponseTransformer.handleMxFaultResponse(faultApiResponse.getStatusCode(), faultApiResponse.getResultJson(), parameters);
         LOGGER.debug("Mm NonRoutine/LogBook fault Response Json {} ", faultResponseJson);
         return ResponseUtils.mapResponseToAurenaRequestedFormat("FaultProjectionService", faultResponseJson);

      } catch (SQLException ex) {
         throw new ProjectionException(ex.getMessage(), ex);
      } catch (Exception ex) {
         LOGGER.error("Error occured.", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      }
   }
   
   @Override
   public Map<String, Object> evaluateNonRoutineService(Map<String, Object> parameters, Connection connection) {

      FaultProjectionHelper evaluateNonRoutine = new FaultProjectionHelper(connection);
      try {
         // Evaluate Non Routine in MM
         LOGGER.debug("EvaluateNonRoutineService FLM request param: {}", parameters.toString());
         evaluateNonRoutine.evaluateNonRoutineInMM(parameters);

         String faultAltId = parameters.get("AltId").toString();
         
         // Evaluate Non Routine in Mx
         JsonObject evaluateNrRequestPayloadJson = buildEvaluateNrRequestBody(faultAltId).build();
         LOGGER.debug("Evaluate Non Routine Request json: {}", evaluateNrRequestPayloadJson.toString());
   
         ApiRequest apiRequest = new ApiRequest(MTX_FAULT_API_PATH, evaluateNrRequestPayloadJson);
         apiRequest.addHeader(IfsCloudFlowHeader.MEX_EDIT_FAULT);
            
         ApiResponse nonRoutineApiResponse = MaintenixApiProxy.post(apiRequest);
         LOGGER.debug("Evaluate Non Routine Api Response status code: {} response json: {}", nonRoutineApiResponse.getStatusCode(), nonRoutineApiResponse.getResultJson());

         LOGGER.debug("Mm Evaluate Non Routine Response Json: {}", nonRoutineApiResponse.getStatusCode(), nonRoutineApiResponse.getResultJson());
         evaluateNonRoutine.handleEvaluateNrResponse(nonRoutineApiResponse.getStatusCode(), nonRoutineApiResponse.getResultJson(), parameters);
         
      } catch (SQLException ex) {
         throw new ProjectionException(ex.getMessage(), ex);
      } catch (Exception ex) {
         LOGGER.error("Error occured.", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      }
      return null;
   }
   
   public JsonObjectBuilder buildEvaluateNrRequestBody(final String faultAltId) {
      JsonObjectBuilder bodyBuilder = Json.createObjectBuilder()
              .add(EVALUATED, true);
      
      JsonObjectBuilder createObjectBuilder = Json.createObjectBuilder()
              .add(REQUEST, Json.createObjectBuilder()
              .add(METHOD, PUT)
              .add(HEADERS, Json.createObjectBuilder()
                       .add(CONTENT_TYPE, Json.createArrayBuilder()
                               .add(APPLICATION_VND_IFS_AMAPI_V_2_JSON))
                       .add(ACCEPT, Json.createArrayBuilder()
                               .add(APPLICATION_VND_IFS_AMAPI_V_2_JSON)))
              .add(URL, MTX_EVALUATE_NON_ROUTINE_API_PATH + faultAltId)
              .add(BODY, bodyBuilder));
           
   
      JsonArrayBuilder apiCalls = Json.createArrayBuilder();
      apiCalls.add(createObjectBuilder);
      return Json.createObjectBuilder().add(API_CALLS, apiCalls);
   }
}