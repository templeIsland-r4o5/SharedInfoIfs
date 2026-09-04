/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmParts
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 */
package com.ifsworld.projection;

import com.ifsworld.adcom.projection.util.EffectiveSensitivitiesResponseTransformer;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import com.ifsworld.mxcore.projection.api.ResponseUtils;
import javax.ejb.Stateless;
import java.sql.Connection;
import java.util.Map;
import org.slf4j.LoggerFactory;

/**
 *
 * Implementation class for all global actions defined in the FlmParts projection model.
 */

@Stateless(name = "FlmPartsFunctions")
public class FlmPartsFunctionsImpl implements FlmPartsFunctions {
   
   private static final org.slf4j.Logger LOGGER = LoggerFactory.getLogger(FlmPartsFunctionsImpl.class);
   
   private static final String MTX_EFFECTIVE_SENSITIVITY_SEARCH_API_PATH = "/amapi/materials/asset/aircraft/{aircraftAltId}/effectivesensitivitiesview";
   
   private static final String AURENA_AIRCRAFT_ALT_ID = "AircraftAltId";
   private static final String AURENA_PART_GROUP_ALT_ID = "PartGroupAltId";
   private static final String ADD_EDIT_PART_SOURCE = "AddEditPart";
   
  

   @Override
   public Map<String, Object> getPartGroupSensitivity(Map<String, Object> parameters, Connection connection) {
      String responseJson = "{}";
 
      String aircraftAltId = (String) parameters.get(AURENA_AIRCRAFT_ALT_ID);
      String partGroupAltId = (String) parameters.get(AURENA_PART_GROUP_ALT_ID);
      
      LOGGER.debug("getPartGroupSensitivity Parameters {}", parameters);
      String apiPath = MTX_EFFECTIVE_SENSITIVITY_SEARCH_API_PATH.replace("{aircraftAltId}", aircraftAltId);
      //Building GET request
      ApiRequest apiRequest = new ApiRequest(apiPath, null);
      apiRequest.withParameter("part_group_id", partGroupAltId);

      ApiResponse sensitivityApiResponse = MaintenixApiProxy.get(apiRequest);
      String sensitivityApiResponseJson = sensitivityApiResponse.getResultJson();
      LOGGER.debug("PGSensitivityApiResponseJson: {}", sensitivityApiResponseJson); 
      
      EffectiveSensitivitiesResponseTransformer.handleHttpResponseStatus(sensitivityApiResponse.getStatusCode());

      responseJson = new EffectiveSensitivitiesResponseTransformer().transformMtxSensitivityResponseJsonIntoIfsProjectionStructure(sensitivityApiResponseJson, ADD_EDIT_PART_SOURCE);
      LOGGER.debug("PGSensitivityResponseJson: {}", responseJson); 
      return ResponseUtils.mapResponseToAurenaRequestedFormat("GetPartGroupSensitivity", responseJson);

   }
   
}
