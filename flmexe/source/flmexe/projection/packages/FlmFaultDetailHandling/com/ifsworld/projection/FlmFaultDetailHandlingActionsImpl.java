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
 *---------------------------------------------------------------------------
 * Date    Sign    Comment
 * ----------------------------------------------------------------------------
 * 240827  RWELLK  AD-13859, Added IfsCloudFlowHeader. 
 * 240714  RWELLK  AD-12997, IS_PHONE_UP_DEFERRAL_ENABLED variable Name has changed.
 * 240714  RWELLK  AD-12997, Done the Modifications related to edit fault MEX and CAMMO integration.
 * 240610  RWELLK  AD-12981, Created and added modifyFaultUtil method.
 * ---------------------------------------------------------------------------
 * ---------------------------------------------------------------------------
 */

package com.ifsworld.projection;

import com.ifsworld.adcom.projection.util.FaultProjectionHelper;
import com.ifsworld.adcom.projection.util.ModifyFaultProjectionHelper;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import java.sql.SQLException;
import java.util.Map;
import javax.ejb.Stateless;
import java.sql.Connection;
import org.slf4j.LoggerFactory;
import org.slf4j.Logger;
import javax.json.JsonObject;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import com.ifsworld.mxcore.projection.api.IfsCloudFlowHeader;
import javax.json.Json;
import javax.json.JsonArrayBuilder;
import javax.json.JsonObjectBuilder;

/**
 * Implementation class for global actions defined in the FlmFaultDetailHandling projection model.
 * 
 * This class implements the `FlmFaultDetailHandlingActions` interface and provides implementations for
 * the defined global actions within the FlmFaultDetailHandling projection model.
 */

@Stateless(name="FlmFaultDetailHandlingActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmFaultDetailHandlingActionsImpl extends FlmFaultDetailHandlingActionsFragmentsWrapper implements FlmFaultDetailHandlingActions {

  
   private static final Logger LOGGER = LoggerFactory.getLogger(FlmFaultDetailHandlingActionsImpl.class);
   private static final String FAULT_ID = "faultId";
   private static final String AM_API_PATH = "amapi/batch";
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
   /**
   * Modifies a fault using the provided parameters
   * 
   * This method delegates the actual fault modification logic to the `RaiseFaultProjectionController` class.
   *  
   * @param parameters A Map containing the fault data to be modified.
   * @throws ProjectionException If an error occurs during fault modification.
   */
   @Override
   public Map<String, Object> modifyFaultService(Map<String, Object> parameters, Connection connection) {
   
      ModifyFaultProjectionHelper modifyFaultProjectionHelper = new ModifyFaultProjectionHelper(connection);
      try {
         String mmFaultId = (String)parameters.get(FAULT_ID);
         LOGGER.debug("Starting to Modify Fault, MM FaultId: {}", mmFaultId);
         //Modify the fault in MM
         modifyFaultProjectionHelper.modifyMmFault(parameters);

         //Edit Fault in Maintenix
         JsonObject modifyFaultPayloadJson = modifyFaultProjectionHelper.transformMxModifyFaultJson(parameters);
         LOGGER.debug("Generated Modify fault request payload: {}", modifyFaultPayloadJson.toString());

         ApiRequest apiRequest = new ApiRequest(AM_API_PATH, modifyFaultPayloadJson);
         apiRequest.addHeader(IfsCloudFlowHeader.MEX_EDIT_FAULT);
         ApiResponse publishFaultApiResponse = MaintenixApiProxy.post(apiRequest);
         LOGGER.debug("Modify fault response, status code: {}, response json: {}", publishFaultApiResponse.getStatusCode(), publishFaultApiResponse.getResultJson());
         modifyFaultProjectionHelper.handleMxRaiseFaultResponse(publishFaultApiResponse.getStatusCode(), publishFaultApiResponse.getResultJson(), parameters);

      } catch (SQLException ex) {
         LOGGER.error("modifyFaultService() SQL error occured ", ex);
         throw new ProjectionException(ex.getMessage(),ex);
      }
       catch (Exception ex) {
         LOGGER.error("modifyFaultService() Error occured ", ex);
         throw new ProjectionException(ex.getMessage());
      } 
     return null;
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
   
         ApiRequest apiRequest = new ApiRequest(AM_API_PATH, evaluateNrRequestPayloadJson);
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