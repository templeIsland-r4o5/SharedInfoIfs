/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmAircraftTurnsDetailsHandling
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------

 * ---------------------------------------------------------------------------
 * Date    Sign     Comment
 * ----------------------------------------------------------------------------
 * 240827  RWELLK  AD-13859, Added IfsCloudFlowHeader. 
 * 240823  CAARLK  AD-13990, Got return response from handleMxRaiseFaultResponse.
 * ---------------------------------------------------------------------------
 */

package com.ifsworld.projection;

import com.ifsworld.adcom.projection.util.FaultProjectionHelper;
import com.ifsworld.adcom.projection.util.FaultRequestTransformer;
import com.ifsworld.adcom.projection.util.FaultResponseTransformer;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import com.ifsworld.mxcore.projection.api.ResponseUtils;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.IfsCloudFlowHeader;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.Map;
import javax.json.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/*
 * Implementation class for all global actions defined in the FlmAircraftTurnsDetailsHandling projection model.
 */

@Stateless(name="FlmAircraftTurnsDetailsHandlingActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmAircraftTurnsDetailsHandlingActionsImpl extends FlmAircraftTurnsDetailsHandlingActionsFragmentsWrapper implements FlmAircraftTurnsDetailsHandlingActions {
   private static final Logger LOGGER = LoggerFactory.getLogger(FlmAircraftTurnsDetailsHandlingActionsImpl.class);
   private static final String MTX_FAULT_API_PATH = "amapi/batch";
           
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
}
