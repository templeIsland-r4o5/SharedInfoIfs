/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: InventoryServiceManager
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 */
package com.ifsworld.projection;

import com.ifsworld.adcom.projection.util.CmsDryRunApiRequestTransformer;
import com.ifsworld.adcom.projection.util.CmsDryRunApiResponseTransformer;
import com.ifsworld.adcom.projection.util.CmsRequest;
import com.ifsworld.adcom.projection.util.InventorySearchResponseTransformer;
import com.ifsworld.adcom.projection.util.HttpStatusCode;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import com.ifsworld.mxcore.projection.api.ResponseUtils;
import javax.ejb.Stateless;
import java.sql.Connection;
import java.util.Map;
import javax.json.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/*
 * Implementation class for all global functions defined in the InventoryServiceManager projection model.
 * Note: Functions should not change database state!
 */
@Stateless(name = "InventoryServiceManagerFunctions")
public class InventoryServiceManagerFunctionsImpl implements InventoryServiceManagerFunctions {

   private static final Logger LOGGER = LoggerFactory.getLogger(InventoryServiceManagerFunctionsImpl.class);

   // Constant for Inventory search API path
   private static final String MTX_INVENTORY_SEARCH_API_PATH = "/amapi/materials/asset/inventory";

   private static final String MTX_CMS_API_PATH = "/cmsApi/currentConfiguration/v1/changeConfiguration/batch";

   // Constants for getRemovalInfoService parm keys
   private static final String AURENA_HIGHEST_INV_ID_REQUEST_PARAM = "HighestInvId";
   private static final String AURENA_CONFIG_SLOT_CODE_REQUEST_PARAM = "ConfigSlotCode";
   private static final String AURENA_CONFIG_SLOT_POSITION_REQUEST_PARAM = "ConfigSlotPosition";
   private static final String AURENA_ASSEMBLY_CONFIG_SLOT_CODE_REQUEST_PARAM = "AssemblyConfigSlotCode";
   private static final String AURENA_ASSEMBLY_CONFIG_SLOT_POSITION_REQUEST_PARAM = "AssemblyConfigSlotPosition";
   
   // Constant for getMtxPartInventoryService param key
   private static final String AURENA_BARCODE_REQUEST_PARAM = "Barcode";
   
   // Constant for MTX response key      
   private static final String MTX_INVENTORY_SEARCH_API_BARCODE_PARAM_KEY = "barcode";

   @Override
   public Map<String, Object> getRemovalInfoService(Map<String, Object> parameters, Connection connection) {
      LOGGER.debug("Parameters {}", parameters);

      String responseJson = "{}";

      //Fetching parameters
      String highestInventoryId = (String) parameters.get(AURENA_HIGHEST_INV_ID_REQUEST_PARAM);
      String configSlotCode = (String) parameters.get(AURENA_CONFIG_SLOT_CODE_REQUEST_PARAM);
      String configSlotPosition = (String) parameters.get(AURENA_CONFIG_SLOT_POSITION_REQUEST_PARAM);
      String assemblyConfigSlotCode = (String) parameters.get(AURENA_ASSEMBLY_CONFIG_SLOT_CODE_REQUEST_PARAM);
      String assemblyConfigSlotPosition = (String) parameters.get(AURENA_ASSEMBLY_CONFIG_SLOT_POSITION_REQUEST_PARAM);

      //Building GET request
      ApiRequest apiRequest = new ApiRequest(MTX_INVENTORY_SEARCH_API_PATH, null);
      apiRequest.withParameter("highest_inv_id", highestInventoryId);
      apiRequest.withParameter("configuration_slot_code", configSlotCode);
      apiRequest.withParameter("configuration_slot_position_name", configSlotPosition);
      if (!isNullOrEmpty(assemblyConfigSlotCode) && !isNullOrEmpty(assemblyConfigSlotPosition)) {
         apiRequest.withParameter("assembly_configuration_slot_code", assemblyConfigSlotCode);
         apiRequest.withParameter("assembly_configuration_slot_position_name", assemblyConfigSlotPosition);
      }

      //Sending GET request
      ApiResponse inventorySearchApiResponse = MaintenixApiProxy.get(apiRequest);
      String inventoryApiResponseJson = inventorySearchApiResponse.getResultJson();
      LOGGER.debug("MTX inventorySearchAPI/HighestInventoryId={} ConfigSlotCode={}  Response: {}", new Object[]{highestInventoryId, configSlotCode, inventoryApiResponseJson});

      HttpStatusCode.handleHttpResponseStatus(inventorySearchApiResponse.getStatusCode());
      
      //Reading request
      responseJson = new InventorySearchResponseTransformer().transformMtxInventorySearchResponseJsonIntoIfsProjectionStructure(inventoryApiResponseJson);

      LOGGER.debug("Return responseJson :  {}", responseJson);
         
      //Mapping request to Aurena response and returning it
      return ResponseUtils.mapResponseToAurenaRequestedFormat("GetRemovalInfoService", responseJson);
   }

   /**
    * Checks if a string is null or empty.
    *
    * @param str The string to check.
    * @return True if the string is null or empty, false otherwise.
    */
   private boolean isNullOrEmpty(String str) {
      return str == null || str.trim().isEmpty() || str.equals("null");
   }

   @Override
   public Map<String, Object> listCmsDryRunWarningService(Map<String, Object> parameters, Connection connection) {
      LOGGER.debug("listCmsDryRunWarningService FLM request param: {}", parameters.toString());

      CmsDryRunApiRequestTransformer cmsDryRunRequestTransformer = new CmsDryRunApiRequestTransformer();
      JsonObject cmsRequestPayloadJson = cmsDryRunRequestTransformer.transformCmsDryRunPayload(parameters);
      LOGGER.debug("Transformed Mtx cms Request json: {}", cmsRequestPayloadJson.toString());

      ApiRequest apiRequest = new ApiRequest(MTX_CMS_API_PATH, cmsRequestPayloadJson);
      apiRequest.withParameter(CmsRequest.MTX_CMS_API_PARAM_DRYRUN_KEY, CmsRequest.MTX_CMS_API_PARAM_DRYRUN_TRUE_VALUE);
      ApiResponse cmsApiResponse = MaintenixApiProxy.post(apiRequest);
      LOGGER.debug("Mtx cms Api Response json: {}", cmsApiResponse.getResultJson());
      
      CmsDryRunApiResponseTransformer cmsDryRunApiResponseTransformer = new CmsDryRunApiResponseTransformer();
      String cmsWarningsJson = cmsDryRunApiResponseTransformer.transformMtxCmsResponseJsonIntoIfsProjectionStructure(cmsApiResponse.getResultJson(), cmsApiResponse.getStatusCode());
      LOGGER.debug("Transformed cms projection Response json: {}", cmsWarningsJson);

      return ResponseUtils.mapResponseToAurenaRequestedFormat("ListCmsDryRunWarningService", cmsWarningsJson);
   }

   @Override
   public Map<String, Object> cmsDryRunResponseSeverityService(Map<String, Object> parameters, Connection connection) {
      LOGGER.debug("CmsDryRunResponseSeverityService FLM request param: {}", parameters.toString());

      CmsDryRunApiRequestTransformer cmsDryRunRequestTransformer = new CmsDryRunApiRequestTransformer();
      JsonObject cmsRequestPayloadJson = cmsDryRunRequestTransformer.transformCmsDryRunPayload(parameters);
      LOGGER.debug("Transformed Mtx cms Request json: {}", cmsRequestPayloadJson.toString());
      
      ApiRequest apiRequest = new ApiRequest(MTX_CMS_API_PATH, cmsRequestPayloadJson);
      apiRequest.withParameter(CmsRequest.MTX_CMS_API_PARAM_DRYRUN_KEY, CmsRequest.MTX_CMS_API_PARAM_DRYRUN_TRUE_VALUE);
      ApiResponse cmsApiResponse = MaintenixApiProxy.post(apiRequest);
      LOGGER.debug("Mtx cms Api Response json: {}", cmsApiResponse.getResultJson());
      
      CmsDryRunApiResponseTransformer cmsDryRunApiResponseTransformer = new CmsDryRunApiResponseTransformer();
      String cmsDryRunResponseSeverityJson = cmsDryRunApiResponseTransformer.transformCmsResponseIntoSeverityJson(cmsApiResponse.getResultJson(), cmsApiResponse.getStatusCode());
      LOGGER.debug("Transformed cms Severity projection Response json: {}", cmsDryRunResponseSeverityJson);
      
      return ResponseUtils.mapResponseToAurenaRequestedFormat("CmsDryRunResponseSeverityService", cmsDryRunResponseSeverityJson);
   }
   
    @Override
   public Map<String, Object> getMtxPartInventoryService(Map<String, Object> parameters, Connection connection) {
      LOGGER.debug("Parameters {}", parameters);
      String responseJson = "{}";

      //Fetching parameter
      String barcode = (String) parameters.get(AURENA_BARCODE_REQUEST_PARAM);
      
      //Building GET request
      ApiRequest apiRequest = new ApiRequest(MTX_INVENTORY_SEARCH_API_PATH, null);
      apiRequest.withParameter(MTX_INVENTORY_SEARCH_API_BARCODE_PARAM_KEY, barcode);

      //Sending GET request
      ApiResponse inventorySearchApiResponse = MaintenixApiProxy.get(apiRequest);
      String inventoryApiResponseJson = inventorySearchApiResponse.getResultJson();
      LOGGER.debug("MTX inventorySearchAPI/barcode={} Response: {}", new Object[]{barcode, inventoryApiResponseJson});

      HttpStatusCode.handleHttpResponseStatus(inventorySearchApiResponse.getStatusCode());
      
      if (isNullOrEmpty(barcode) && (inventorySearchApiResponse.getStatusCode() == HttpStatusCode.NOT_FOUND)) {
         LOGGER.debug("Received null or empty for barcode");
         responseJson = new InventorySearchResponseTransformer().transformMtxInventorySearchResponseJsonIntoIfsProjectionStructure("[]");
      } else {
         //Reading request
         responseJson = new InventorySearchResponseTransformer().transformMtxInventorySearchResponseJsonIntoIfsProjectionStructure(inventoryApiResponseJson);
      }
          
      LOGGER.debug("Return response Json: {}", responseJson);

      //Mapping request to Aurena response and returning it
      return ResponseUtils.mapResponseToAurenaRequestedFormat("GetMtxPartInventoryService", responseJson);
   }
}
