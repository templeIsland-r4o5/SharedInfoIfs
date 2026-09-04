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

import com.ifsworld.adcom.projection.util.FaultDeferralProjectionHelper;
import com.ifsworld.adcom.projection.util.MxDeferralAlertController;
import com.ifsworld.adcom.projection.util.MxPartRequirementRequest;
import com.ifsworld.adcom.projection.util.MxToolRequirementRequest;
import com.ifsworld.adcom.projection.util.MxMeasurementRequirementRequest;
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
import java.util.List;
import java.util.Map;
import javax.json.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/*
 * Implementation class for all global actions defined in the FlmFaultDeferral projection model.
 */
@Stateless(name = "FlmFaultDeferralActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmFaultDeferralActionsImpl implements FlmFaultDeferralActions {

   private static final Logger LOGGER = LoggerFactory.getLogger(FlmFaultDeferralActionsImpl.class);
   public static final String AMAPI_SYS_ALERT = "amapi/sys/alert";
   public static final String AMAPI_BATCH = "amapi/batch";

   @Override
   public Map<String, Object> faultDeferralService(final Map<String, Object> parameters, final Connection connection) {
      FaultDeferralProjectionHelper deferFaultService = new FaultDeferralProjectionHelper(connection);
      try {
         // Step 1 - Defer Fault in MM
         String mmDeferFaultResponseJson = deferFaultService.deferFault(parameters);
         LOGGER.debug("Response json {} ", mmDeferFaultResponseJson);

         String mxFaultStatus = (String) parameters.get("MxFaultStatus");
         LOGGER.debug("Mx fault status is {} ", mxFaultStatus);

         if (mxFaultStatus.equals("Open") || mxFaultStatus.isEmpty()) {
            // Step 2 - Defer Fault in Mx
            Map<String, Object> result = deferFaultService.transformMxDeferFaultJson(parameters);
            JsonObject deferFaultPayloadJson = (JsonObject) result.get("jsonPayload");
            List<MxPartRequirementRequest> mxPartRequirementRequests = (List<MxPartRequirementRequest>) result.get("partRequirementRequests");
            List<MxToolRequirementRequest> mxToolRequirementRequest = (List<MxToolRequirementRequest>) result.get("toolRequirementRequests");
            List<MxMeasurementRequirementRequest> mxMeasurementRequirementRequests = (List<MxMeasurementRequirementRequest>) result.get("measurementRequirementRequests");
            LOGGER.debug("Generated defer fault request payload: {}", deferFaultPayloadJson.toString());
            ApiRequest apiRequest = new ApiRequest(AMAPI_BATCH, deferFaultPayloadJson);
            apiRequest.addHeader(IfsCloudFlowHeader.MEX_DEFER_FAULT);
            ApiResponse publishDeferFaultApiResponse = MaintenixApiProxy.post(apiRequest);
            LOGGER.debug("Defer fault response status code: {} response json: {}", publishDeferFaultApiResponse.getStatusCode(), publishDeferFaultApiResponse.getResultJson());

            // Step 3 - Persist Mx Keys on MM entities
            try {
               deferFaultService.handleMxDeferFaultResponse(publishDeferFaultApiResponse.getStatusCode(), publishDeferFaultApiResponse.getResultJson(), parameters, mxPartRequirementRequests, mxToolRequirementRequest, mxMeasurementRequirementRequests);
            } catch (ProjectionException pe) {
               // Raise an MX alert when a deferral failure occurs in MX.
               LOGGER.error("ProjectionException caught while handling Mx defer fault response: {}", pe.getMessage());
               raiseMxDeferralAlert(parameters, pe.getMessage());
            }
         } else {
            //Since the corresponding fault in MX is not in the Open status, raise an alert in MX
            raiseMxDeferralAlert(parameters, null);
         }
         return ResponseUtils.mapResponseToAurenaRequestedFormat("FaultDeferralService", mmDeferFaultResponseJson);
      } catch (SQLException ex) {
         LOGGER.error("SQL error occured ", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      } catch (Exception ex) {
         LOGGER.error("Error occured ", ex);
         throw new ProjectionException(ex.getMessage());
      }
   }

   private void raiseMxDeferralAlert(Map<String, Object> parameters, String cause) throws Exception {
      MxDeferralAlertController mxDeferralAlertController = new MxDeferralAlertController();
      JsonObject mxDeferralAlertPayloadJson = mxDeferralAlertController.transformMxDeferralAlertJson(parameters, cause);
      LOGGER.debug("Generated alert request payload: {}", mxDeferralAlertPayloadJson.toString());
      ApiRequest apiRequest = new ApiRequest(AMAPI_SYS_ALERT, mxDeferralAlertPayloadJson);
      ApiResponse raiseMxDeferralAlertResponse = MaintenixApiProxy.post(apiRequest);
      LOGGER.debug("Alert response status code: {} response json: {}", raiseMxDeferralAlertResponse.getStatusCode(), raiseMxDeferralAlertResponse.getResultJson());
      mxDeferralAlertController.handleMxDeferralAlertResponse(raiseMxDeferralAlertResponse.getStatusCode(), raiseMxDeferralAlertResponse.getResultJson());
   }
}
