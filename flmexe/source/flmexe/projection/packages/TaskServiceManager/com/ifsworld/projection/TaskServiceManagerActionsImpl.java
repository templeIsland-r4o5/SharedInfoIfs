package com.ifsworld.projection;

import com.ifsworld.adcom.projection.util.FaultBatchAPIParam;
import com.ifsworld.adcom.projection.util.HttpStatusCode;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import com.ifsworld.mxcore.projection.api.ApiRequest;
import com.ifsworld.mxcore.projection.api.ApiResponse;
import com.ifsworld.mxcore.projection.api.IfsCloudFlowHeader;
import com.ifsworld.mxcore.projection.api.MaintenixApiProxy;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import java.sql.Connection;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import javax.json.Json;
import javax.json.JsonArrayBuilder;
import javax.json.JsonObject;
import javax.json.JsonObjectBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/*
 * Implementation class for all global functions defined in the InventoryServiceManager projection model.
 * Note: Functions should not change database state!
 */
@Stateless(name = "TaskServiceManagerActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class TaskServiceManagerActionsImpl implements TaskServiceManagerActions {

   private static final Logger LOGGER = LoggerFactory.getLogger(TaskServiceManagerActionsImpl.class);
   private static final String MTX_AM_API_PATH = "amapi/batch";
   private static final String USER = "erp/hr/user";

   private static final String REQUEST = "request";
   private static final String METHOD = "method";
   private static final String GET = "GET";
   private static final String PUT = "PUT";
   private static final String HEADERS = "headers";
   private static final String ACCEPT = "Accept";
   private static final String APPLICATION_JSON = "application/json";
   private static final String URL = "url";
   private static final String BODY = "body";
   private static final String CONTENT_TYPE = "Content-Type";

   @Override
   public Map<String, Object> addTaskActionService(Map<String, Object> parameters, Connection connection) {
      LOGGER.debug("Parameters {}", parameters);

      try {
         TaskActionDTO taskAction = createTaskActionDTO(parameters);
         JsonObject taskActionRequest = createTaskActionRequest(taskAction);

         ApiResponse taskActionResponse = sendTaskActionRequest(taskActionRequest);
         LOGGER.debug("Evaluate Non Routine Api Response status code: {} response json: {}", taskActionResponse.getStatusCode(), taskActionResponse.getResultJson());

         processResponse(taskActionResponse.getStatusCode());
      } catch (Exception ex) {
         LOGGER.error("Error occurred.", ex);
         throw new ProjectionException(ex.getMessage(), ex);
      }
      return null;
   }

   private TaskActionDTO createTaskActionDTO(Map<String, Object> parameters) {
      TaskActionDTO taskAction = new TaskActionDTO();
      taskAction.setDescription(parameters.get("Description").toString());
      taskAction.setDate(LocalDateTime.parse(parameters.get("ActionDate").toString(), DateTimeFormatter.ISO_LOCAL_DATE_TIME).atZone(ZoneOffset.UTC).toInstant().toString());
      taskAction.setUsername(parameters.get("Username").toString());
      taskAction.setTaskAltId(parameters.get("TaskAltId").toString());
      return taskAction;
   }

   private JsonObject createTaskActionRequest(TaskActionDTO taskAction) {
      JsonArrayBuilder apiCalls = Json.createArrayBuilder();
      apiCalls.add(buildGetUserRequest(taskAction));
      apiCalls.add(buildTaskRequest(taskAction));

      return Json.createObjectBuilder().add(FaultBatchAPIParam.API_CALLS, apiCalls).build();
   }

   private JsonObjectBuilder buildGetUserRequest(TaskActionDTO taskAction) {
      String url = USER + "?username=" + taskAction.getUsername();
      return Json.createObjectBuilder()
              .add(FaultBatchAPIParam.REQUEST, Json.createObjectBuilder()
                      .add(FaultBatchAPIParam.METHOD, GET)
                      .add(HEADERS, Json.createObjectBuilder()
                              .add(CONTENT_TYPE, Json.createArrayBuilder()
                                      .add(APPLICATION_JSON))
                      )
                      .add(FaultBatchAPIParam.URL, url)
                      .addNull(FaultBatchAPIParam.BODY));
   }

   private JsonObjectBuilder buildTaskRequest(TaskActionDTO taskAction) {
      String taskURL = "maintenance/exec/task/" + taskAction.getTaskAltId();

      return Json.createObjectBuilder()
              .add(REQUEST, Json.createObjectBuilder()
                      .add(METHOD, PUT)
                      .add(HEADERS, Json.createObjectBuilder()
                              .add(CONTENT_TYPE, Json.createArrayBuilder()
                                      .add(APPLICATION_JSON))
                              .add(ACCEPT, Json.createArrayBuilder()
                                      .add(APPLICATION_JSON)))
                      .add(URL, taskURL)
                      .add(BODY, buildTaskRequestBody(taskAction)));
   }

   private JsonObjectBuilder buildTaskRequestBody(TaskActionDTO taskAction) {
      return Json.createObjectBuilder().add(FaultBatchAPIParam.ACTIONS, buildCorrectiveAction(taskAction));
   }

   private JsonArrayBuilder buildCorrectiveAction(TaskActionDTO taskAction) {
      JsonArrayBuilder arrayBuilder = Json.createArrayBuilder();
      JsonObjectBuilder jsonObjectBuilder = Json.createObjectBuilder();
      jsonObjectBuilder.add(FaultBatchAPIParam.CORR_DESCRIPTION, taskAction.getDescription());
      jsonObjectBuilder.add(FaultBatchAPIParam.CORR_ACTION_DATE, taskAction.getDate());      
      jsonObjectBuilder.add(FaultBatchAPIParam.CORR_USER_ID, "{result=0:$.[0].id}");
      
      return arrayBuilder.add(jsonObjectBuilder);
   }

   private ApiResponse sendTaskActionRequest(JsonObject taskActionRequest) throws Exception {
      ApiRequest apiRequest = new ApiRequest(MTX_AM_API_PATH, taskActionRequest);
      apiRequest.addHeader(IfsCloudFlowHeader.MEX_EDIT_FAULT);
      return MaintenixApiProxy.post(apiRequest);
   }

   private void processResponse(int statusCode) throws SQLException, Exception {
      if (statusCode != HttpStatusCode.STATUS_OK) {
         throw new ProjectionException("Error occoured while processing request");
      }
   }

   private class TaskActionDTO {

      private String taskAltId;
      private String username;
      private String description;
      private String date;

      public String getTaskAltId() {
         return taskAltId;
      }

      public void setTaskAltId(String taskAltId) {
         this.taskAltId = taskAltId;
      }

      public String getUsername() {
         return username;
      }

      public void setUsername(String username) {
         this.username = username;
      }

      public String getDescription() {
         return description;
      }

      public void setDescription(String description) {
         this.description = description;
      }

      public String getDate() {
         return date;
      }

      public void setDate(String date) {
         this.date = date;
      }
   }
}
