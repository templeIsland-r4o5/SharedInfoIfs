/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmFaultDetailHandling
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 */

package com.ifsworld.projection;

import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import com.ifsworld.mxcore.projection.api.ResponseUtils;
import com.ifsworld.adcom.projection.util.EffectiveSensitivitiesResponseTransformer;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import javax.ejb.Stateless;
import java.io.InputStream;
import java.sql.Connection;
import java.util.Map;
import org.slf4j.LoggerFactory;

/*
 * Implementation class for all global functions defined in the FlmFaultDetailHandling projection model.
 * Note: Functions should not change database state!
 */

@Stateless(name="FlmFaultDetailHandlingFunctions")
public class FlmFaultDetailHandlingFunctionsImpl extends FlmFaultDetailHandlingFunctionsFragmentsWrapper implements FlmFaultDetailHandlingFunctions {
   private static final org.slf4j.Logger LOGGER = LoggerFactory.getLogger(FlmRaiseFaultFunctionsImpl.class);
   private static final String MTX_EFFECTIVE_SENSITIVITY_SEARCH_API_PATH = "/amapi/materials/asset/aircraft/{aircraftAltId}/effectivesensitivitiesview";
   private static final String AURENA_CONFIG_SLOT_ALT_ID = "ConfigSlotAltId";
   private static final String AURENA_AIRCRAFT_ALT_ID = "AircraftAltId";
   @Override
   public Map<String, Object> getFailedSystemSensitivity(final Map<String, Object> parameters, final Connection connection) {
      LOGGER.debug("Parameters {}", parameters);
      String responseJson = "{}";
      
      //Fetching parameters
      String aircraftAltId = (String) parameters.get(AURENA_AIRCRAFT_ALT_ID);
      String configSlotAltId = (String) parameters.get(AURENA_CONFIG_SLOT_ALT_ID);

      try{
         String finalApiPath=MTX_EFFECTIVE_SENSITIVITY_SEARCH_API_PATH.replace("{aircraftAltId}", aircraftAltId);
         //Building GET request
         ApiRequest apiRequest = new ApiRequest(finalApiPath, null);
         apiRequest.withParameter("is_etops", false);
         apiRequest.withParameter("configuration_slot_id", configSlotAltId);

         //Sending GET request
         ApiResponse sensitivityApiResponse = MaintenixApiProxy.get(apiRequest);
         String sensitivityApiResponseJson = sensitivityApiResponse.getResultJson();
         LOGGER.debug("APIResponseJson: {}", sensitivityApiResponseJson); 

         EffectiveSensitivitiesResponseTransformer.handleHttpResponseStatus(sensitivityApiResponse.getStatusCode());

         responseJson = new EffectiveSensitivitiesResponseTransformer().transformMtxSensitivityResponseJsonIntoIfsProjectionStructure(sensitivityApiResponseJson, "RaiseFaultAssistant");
         LOGGER.debug("ResponseJson: {}", responseJson);

         //Mapping request to Aurena response and returning it
         return ResponseUtils.mapResponseToAurenaRequestedFormat("GetFailedSystemSensitivity", responseJson);
      } catch (Exception ex) {
         LOGGER.error("Error occured.", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      }
   }
}