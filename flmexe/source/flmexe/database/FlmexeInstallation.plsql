-----------------------------------------------------------------------------
--
--  Logical unit: FlmexeInstallation
--  Component:    FLMEXE
--
--  IFS Developer Studio Template Version 3.0
--
--  Date    Sign    History
--  ------  ------  ---------------------------------------------------------
--  251108  ALNILK  AD-21532, Updated the projection grants
--  250829  NIRTLK  AD-19210, Granted FlmPartTagReportArchiveHandling for MM_TECHNICIAN,MM_SUPERVISOR,HANGAR_TECHNICIAN and HANGAR_SUPERVISOR.
--  250829  NIRTLK  AD-19621, Granted ServiceableTagRep,UnserviceableTagRep,QuarantineTagRep for MM_TECHNICIAN,MM_SUPERVISOR,HANGAR_TECHNICIAN and HANGAR_SUPERVISOR.
--  250825  VAALLK  AD-18953, Update to grant permission for MeasurementLineVirtual
--  250714  SSIVLK  AD-20135, Granted InventoryPartInStockHandling for line , hangar technician & supervisor
--  250714  SSIVLK  AD-19194, Granted MxPartDefinitionSearchHandling,MxInventorytSearchHandling for line technician & supervisor
--  250617  NIRTLK  AD-18329, Granted LMShiftHandoverReportRep for MM_SUPERVISOR.
--  250602  NIRTLK  AD-18329, Granted HMShiftHandoverReportRep for HANGAR_CREW_LEAD and HANGAR_SUPERVISOR.
--  250526  SRLALK  AD-18264, Updated PROJECT_MANAGER, INVOICE_AGENT, and HANGAR_CUST_RELSHIP_MANAGER pemisson sets.
--  250526  VAALLK  AD-18260, Grant FlmTaskDetailHandling to hangar planner role.
--  250521  KOSRUS  AD-18208, Granted FlmCriticalItemSeveritiesHandling projection to HANGAR_SUPERVISOR,HANGAR_CREW_LEAD,MM_ADMIN
--  250502  VAALLK  AD-18257, Created HANGAR_PROD_PLANNER permission set.
--  250411  VAALLK  AD-18245, Created HANGAR_CUST_RELSHIP_MANAGER permission set.
--  250311  MAILLK  AD-17731, Updated  Hangar Technician, Hangar Supervisor and Hangar Crew Lead permission sets with Esig permissions
--  250128  BACHLK  AD-14746, Update to regrant MM_TECHNICIAN permission set.
--  250128  WIJCLK  AD-15471, Granted Projections To Hangar Technician
--  250115  MAJSLK  AD-16262, Granted FlmNonRoutinesOfWorkPackageHandling projection to HANGAR_SUPERVISOR, HANGAR_TECHNICIAN
--  241210  MAJSLK  AD-14747, Update to regrant HANGAR_SUPERVISOR, HANGAR_TECHNICIAN permission sets
--  241031  KAWJLK  AD-15283, Remove Deprecated DOCMAN_DIGITAL_SIGNATURES Role. 
--  241009  NIRTLK  AD-14472, Added FNDGPT_RUNTIME permission set to MM_TECHNICIAN
--  240917  VAALLK  AD-14222, Update to regrant MM_ADMINISTRATOR permission set
--  240724  BACHLK  AD-13686, Update to regrant projection permission with CMS commands for Task/Fault DetailsHandling
--  240613  LAHNLK  AD-12996, Update to regrant projection permission  with java - projections FlmAircraftTurnsDetailsHandling-projection
--  240611  PSUALK  AD-12718, Update to regrant projection permission  with suppportwarning property Task/Fault DetailsHanding
--  240509  RAFALK  AD-12571, Gtanted FlmFluidConsumptionLobbyHandling projection to MM_ADMIN
--  240424  KAPALK  AD-12568, Granted FlmMocLobbyHandling projection to MOC
--  240418  ROERLK  AD-12569, Granted FlmLineWorkManagementLobbyHandling projection to MM_SUPERVISOR
--  240416  KAWJLK  AD-12564, Granted AvEsignLogoHandling projection to MM_ADMINSTRATOR.
--  240417  WAISLK  AD-12567, Granted FlmTechnicianLobbyHandling projection to MM_TECHNICIAN and MM_SUPERVISOR.
--  240220  SATGLK  AD-10956, Granted AdAircraftOverdueMaintenanceDetailsHandling projection to MM_MAINT_OPERATIONS_CONTROLLER.
--  240219  VAALLK  AD-11917, Granted MxFaultDetailHandling projection to MM_TECHNICIAN & MM_MAINT_OPERATIONS_CONTROLLER.
--  240217  SATGLK  AD-10947, Added MM_OVERRIDE_HARD_STOP permission set
--  240214   majslk  AD-12145, Modified MM permission sets with IFS_MANAGED delivery type
--  240117  roerlk  AD-11359, Added FlmFaultSearchHandling to MM_TECHNICIAN permission set.
--  231023  majslk  AD-11011, Added MediaLibraryAttachmentHandling to MM_TECHNICIAN permission set.
--  230926  waislk  AD-10835, Remove access of FlmWorkManagementNavigator,FlmResourceAllocationGanttHandling and lobbyPaged222b6cd-42e3-4f77-8b06-a891a635b6d4 for technician.
--  230925  Satglk  AD-10779, Granted Technician Lobby to Supervisor.
--  230921  majslk  AD-10760, Modified Post_Installation_Import_Data to add missing grants and lobbies.
--  230907  SRCHLK  AD-9734, Created MM_FLIGHT_API permission set.
--  230822  PSUALK  AD-9546, Rename permission set DOCUMENT_ATTACHMENT_AURENA / DOCUMENT_ATTACHMENT_AURENA_B2B. 
--  230804  WAISLK  AD-10242, Granted EventActionHandling projection to MM_ADMINISTRATOR permission set. 
--  230628  KAWJLK  AD-10042, Added Post_Installation_Import_Data method to resolve grant lobbies issue in a fresh installation.
--  230613  SRCHLK  AD-9623, Removed an unwanted projection grant.
--  230609  SRCHLK  AD-9623, Added missing projections.
--  230602  SRCHLK  AD-9623, Created MM_ADMINISTRATOR and MM_LINE_PLANNER permission sets.
--  230601  JIWELK  AD-9971, Updated Do_Line_Technician_Grants___ and Do_MOC_Grants___ procedures to call Security_SYS.Create_Role in order to allow updates, Remove Create_Permission_Set___ procedure since its not used.
--  230104  DUWJLK  AD-9283, Updated permission set name of MM_TECHNICIAN in Do_Line_Technician_Grants___ procedure
--  221110  majslk  AD-8724, Updated permission set description of MM_TECHNICIAN
--  221101  rosdlk  AD-8697, Updated MM_TECHNICIAN, MM_MAINT_OPERATIONS_CONTROLLER and MM_SUPERVISOR with turns nav entry permission
--  221123  rosdlk  AD-9047, Updated MOC permission set.
--  221101  rosdlk  AD-8946, Created MM_MAIN_OPERATIONS_CONTROLLER permission set and revoke 'Initiate Deferral' command from technician.
--  221026  majslk  AD-8724, Added missing projections
--  221026  majslk  AD-8724, Created MM_TECHNICIAN permission set
--  221011  lavwlk  AD-8795, Modified FLM_SUPERVISOR role and Forward Line description to MM_SUPERVISOR role and Mobile Maintenance description.
--  220105  rjoslk  AD-4113, Added FLM_SUPERVISOR role.
-----------------------------------------------------------------------------

layer Core;

-------------------- PUBLIC DECLARATIONS ------------------------------------
role_                                      CONSTANT VARCHAR2(50) := 'MM_SUPERVISOR';
technician_role_                           CONSTANT VARCHAR2(30) := 'MM_TECHNICIAN';
admin_role_                                CONSTANT VARCHAR2(30) := 'MM_ADMINSTRATOR';
moc_role_                                  CONSTANT VARCHAR2(30) := 'MM_MAINT_OPERATIONS_CONTROLLER';
override_hard_stop_role_                   CONSTANT VARCHAR2(30) := 'MM_OVERRIDE_HARD_STOP';
hangar_supervisor_role_                    CONSTANT VARCHAR2(30) := 'HANGAR_SUPERVISOR';
hangar_technician_role_                    CONSTANT VARCHAR2(30) := 'HANGAR_TECHNICIAN';
hangar_crew_lead_role_                     CONSTANT VARCHAR2(30) := 'HANGAR_CREW_LEAD';

-------------------- PRIVATE DECLARATIONS -----------------------------------


-------------------- LU SPECIFIC IMPLEMENTATION METHODS ---------------------
@IgnoreUnitTest TrivialFunction
PROCEDURE Grant_Role___ (
   user_role_    VARCHAR2,
   grantee_ VARCHAR2 )
IS
   err_msg_               VARCHAR2(30000);
BEGIN
   Security_SYS.Grant_Role(user_role_, grantee_);
EXCEPTION
   WHEN OTHERS THEN
      err_msg_ := substr(SQLERRM, 1, 3000);
      Dbms_Output.Put_Line('Error when creating user_role: ' || user_role_ || ' for grantee: ' || grantee_);
      Dbms_Output.Put_Line(err_msg_);
END Grant_Role___;

@IgnoreUnitTest NoOutParams
PROCEDURE Grant_Projection___ (
   projection_ VARCHAR2,
   user_role_ VARCHAR2)
IS
BEGIN
   IF Fnd_Projection_API.Exists(projection_) = TRUE THEN
      Fnd_Projection_Grant_API.Grant_All(projection_,user_role_, 'FALSE');
   END IF;
END Grant_Projection___;

@IgnoreUnitTest NoOutParams
PROCEDURE Grant_Proj_Entity___(
   projection_ VARCHAR2,
   entity_     VARCHAR2,
   user_role_       VARCHAR2)
IS 
BEGIN
   IF Fnd_Projection_API.Exists(projection_) = TRUE AND Fnd_Proj_Entity_API.Exists(projection_, entity_) = TRUE THEN 
      
      Fnd_Proj_Entity_Grant_API.Grant_Cud(projection_, entity_, user_role_);
   END IF;
END Grant_Proj_Entity___;

@IgnoreUnitTest NoOutParams
PROCEDURE Grant_Security_Groups___ (
   activity_ VARCHAR2,
   user_role_ VARCHAR2)
IS
BEGIN
   IF (NOT ACTIVITY_GRANT_API.Exists(user_role_, activity_)) THEN
      Security_SYS.Grant_Activity(activity_, user_role_);
   END IF;
END Grant_Security_Groups___;

@IgnoreUnitTest NoOutParams
PROCEDURE Grant_Read_Only_Projection___ (
   projection_ VARCHAR2,
   user_role_ VARCHAR2)
IS
BEGIN
   IF Fnd_Projection_API.Exists(projection_) = TRUE THEN
      Fnd_Projection_Grant_API.Grant_Query(projection_,user_role_);
   END IF;
END Grant_Read_Only_Projection___;

@IgnoreUnitTest NoOutParams
PROCEDURE Grant_Lobby_Page___ (
   page_         VARCHAR2, 
   user_role_         VARCHAR2)
IS
BEGIN
   Security_SYS.Grant_Pres_Object(page_, user_role_);
END Grant_Lobby_Page___;

@IgnoreUnitTest NoOutParams
PROCEDURE Post_Installation_Import_Data 
IS   
BEGIN
   IF Database_SYS.Component_Active('FLMEXE') THEN
      Grant_Role___('MOBILE_APP_RUNTIME', technician_role_);      
      Grant_Role___('FND_MOBILE_APP_SYNC_TRACE', technician_role_);
      Grant_Role___('FNDGPT_RUNTIME', technician_role_);
      
      --Grant Lobby Pages for line technician.
      Grant_Lobby_Page___('lobbyPage32800a3e-6d9a-40a6-8ed5-d71f510ada05', technician_role_);

      --Grant Lobby Page for Admin
      Grant_Lobby_Page___('lobbyPage42f46ace-742f-4186-9e4d-5d730437284b', admin_role_);
      Grant_Lobby_Page___('lobbyPagef36ae1f2-7f6a-4b74-86d1-1adbd7087216', admin_role_);
      Grant_Lobby_Page___('lobbyPage8b4f9361-2f22-40bf-a48f-49b0e4b381d1', admin_role_);
      Grant_Lobby_Page___('lobbyPage60c9811f-595a-4025-a820-69e01c6e31b3', admin_role_);
      Grant_Lobby_Page___('lobbyPagec34b39a9-2a38-4466-9ba5-62f97e013836', admin_role_);
      Grant_Lobby_Page___('lobbyPagec894acb6-caa1-4c76-883f-907712bc7097', admin_role_);

      --Grant Lobby Page for MOC
      Grant_Lobby_Page___('lobbyPage95a7f598-0cae-4e44-ae93-9df74489a45c', moc_role_);
      
      --Grant Lobby Page for line supervisor
      Grant_Lobby_Page___('lobbyPaged222b6cd-42e3-4f77-8b06-a891a635b6d4', role_);
      Grant_Lobby_Page___('lobbyPage32800a3e-6d9a-40a6-8ed5-d71f510ada05', role_);
      
      --Grant Hangar Lobby Page for Hangar Technician
      Grant_Lobby_Page___('lobbyPage8b4f9361-2f22-40bf-a48f-49b0e4b381d1', hangar_technician_role_);
      Grant_Lobby_Page___('lobbyPage60c9811f-595a-4025-a820-69e01c6e31b3', hangar_technician_role_);
      
      --Grant Hangar Lobby Page for Hangar Supervisor
      Grant_Lobby_Page___('lobbyPagec34b39a9-2a38-4466-9ba5-62f97e013836', hangar_supervisor_role_);
      Grant_Lobby_Page___('lobbyPagec894acb6-caa1-4c76-883f-907712bc7097', hangar_supervisor_role_);
      
      --Grant Hangar Lobby Page for Hangar Crew Lead
      Grant_Lobby_Page___('lobbyPage0a9a3fdf-b5e3-4325-ab78-09f1c6ff00e5', hangar_crew_lead_role_);
      Grant_Lobby_Page___('lobbyPage825ea048-87c2-455f-807e-ed6ef203631d', hangar_crew_lead_role_);
   END IF;
END Post_Installation_Import_Data ;


@IgnoreUnitTest NoOutParams
PROCEDURE Do_Line_Technician_Grants___
IS
BEGIN
   
   Security_SYS.Create_Role(technician_role_, 'Access grants for the Line Technician under the Mobile Maintenance Solution', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');  
   Security_SYS.Clear_Role(technician_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', technician_role_);
   Grant_Role___('FND_DSS_ASST_ENDUSER', technician_role_);
   Grant_Role___('MOBILE_APP_RUNTIME', technician_role_);
   Grant_Role___('FND_MOBILE_APP_SYNC_TRACE', technician_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD', technician_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD_B2B', technician_role_);
   Grant_Role___('FND_REM_ASST_ENDUSER', technician_role_);
   
   --Projections for line technician.
   Grant_Projection___('FLMaintApp', technician_role_);
   Grant_Projection___('AdcomNavigator', technician_role_);
   Grant_Projection___('AdmonCommunicationLogHandling',technician_role_);
   Grant_Projection___('AdmonCommunicationLogLevelHandling', technician_role_);
   Grant_Projection___('FlmAircraftTurnsDetailsHandling', technician_role_);
   Grant_Projection___('FlmMyAircraftTurnsHandling', technician_role_);
   Grant_Projection___('FlmMyWorksHandling', technician_role_);
   Grant_Projection___('FlmexeNavigator', technician_role_);
   Grant_Projection___('FlmFaultDetailHandling', technician_role_);
   Grant_Projection___('FlmTaskDetailHandling', technician_role_);
   Grant_Projection___('FlmAircraftTurnsNavigatorEntry', technician_role_);
   Grant_Projection___('MediaLibraryAttachmentHandling', technician_role_);
   Grant_Projection___('FlmFaultSearchHandling', technician_role_);
   Grant_Projection___('MxFaultDetailHandling', technician_role_);
   Grant_Projection___('FlmTechnicianLobbyHandling', technician_role_);
   Grant_Projection___('MxWorkPackageDetailsHandling', technician_role_);
   Grant_Projection___('FlmTaskCardHandling', technician_role_);
   Grant_Projection___('MxPartDefinitionSearchHandling', technician_role_);
   Grant_Projection___('MxInventorytSearchHandling', technician_role_);
   Grant_Projection___('InventoryPartInStockHandling', technician_role_);
   Grant_Projection___('ManualIssueAssistantHandling', technician_role_);
   Grant_Projection___('CfgViewerHandling', technician_role_);
   Grant_Projection___('CfgSubChapterHandling', technician_role_);
   Grant_Projection___('FlmMyPartRequestHandling', technician_role_);
   Grant_Projection___('FlmPartTagReportArchiveHandling', technician_role_);
   Grant_Projection___('ServiceableTagRep', technician_role_);
   Grant_Projection___('UnserviceableTagRep', technician_role_);
   Grant_Projection___('QuarantineTagRep', technician_role_);
   Grant_Projection___('EventLogAttachmentHandling', technician_role_);

   --Grant madatory projections are required for using Maintenix integration 
   Grant_Read_Only_Projection___('AdmonNavigator', technician_role_);
   Grant_Read_Only_Projection___('MxZoneDetailsHandling', technician_role_);
   Grant_Read_Only_Projection___('MxPanelDetailsHandling', technician_role_);

   --Grant Lobby Pages for line technician.
   Grant_Lobby_Page___('lobbyPage32800a3e-6d9a-40a6-8ed5-d71f510ada05', technician_role_);
   
   --Grant Security Groups for line technician.
   Grant_Security_Groups___('FLMaintApp 1.DocumentManagement', technician_role_);
   Grant_Security_Groups___('FLMaintApp 1.FLMaintApp', technician_role_);
   Grant_Security_Groups___('FLMaintApp 1.MediaLibraryManagement', technician_role_);
   Grant_Security_Groups___('FLMaintApp 1.MobileObjectConnectionConfigManagement', technician_role_);
   Grant_Security_Groups___('FLMaintApp 1.ReplaceMediaLibraryItem', technician_role_);
     
END Do_Line_Technician_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_MOC_Grants___
IS
BEGIN
   
   Security_SYS.Create_Role(moc_role_, 'Access grants for the Maintenance Operations Controller under the Mobile Maintenance Solution', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED'); 
   Security_SYS.Clear_Role(moc_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', moc_role_);
   Grant_Role___('FND_DSS_ASST_ENDUSER', moc_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD', moc_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD_B2B', moc_role_);
   
END Do_MOC_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_MM_Admin_Grants___
IS
BEGIN
   
   Security_SYS.Create_Role(admin_role_,'Access grants for an Administrator configuring Mobile Maintenance for end users', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');
   Security_SYS.Clear_Role(admin_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', admin_role_);
   Grant_Role___('DOCMAN_ADMINISTRATOR', admin_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD', admin_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD_B2B', admin_role_);
   Grant_Role___('FND_ADMIN_FNDMIG', admin_role_);
   Grant_Role___('FND_DSS_ASST_ADMIN', admin_role_);
   Grant_Role___('FND_DSS_ASST_ENDUSER', admin_role_);
   Grant_Role___('FND_DSS_ASST_SERVICE', admin_role_);
   Grant_Role___('FND_MOBILE_APP_SYNC_TRACE', admin_role_);
   Grant_Role___('FND_REM_ASST_ADMIN', admin_role_);
   Grant_Role___('FND_REM_ASST_SERVICE', admin_role_);
   Grant_Role___('MOBILE_APP_ADMIN', admin_role_);
 
   --Projections grants for Admin
   Grant_Projection___('AdmonCommunicationLogHandling', admin_role_);
   Grant_Projection___('AdmonCommunicationLogLevelHandling', admin_role_);
   Grant_Projection___('AircraftHandling2', admin_role_);
   Grant_Projection___('AircraftSubSystemHandling', admin_role_);
   Grant_Projection___('AircraftSystemHandling', admin_role_);
   Grant_Projection___('AircraftTypeHandling', admin_role_);
   Grant_Projection___('AircraftWorkPackageHandling', admin_role_);
   Grant_Projection___('AirportHandling', admin_role_);
   Grant_Projection___('AirportSiteHandling', admin_role_);
   Grant_Projection___('AirportsHandling', admin_role_);
   Grant_Projection___('AvAircraftHandling', admin_role_);
   Grant_Projection___('AvAirportForUserHandling', admin_role_);
   Grant_Projection___('AvESigUserPermissionHandling', admin_role_);
   Grant_Projection___('BatchQueueConfigurationHandling', admin_role_);
   Grant_Projection___('BundledMessageViewerHandling', admin_role_);
   Grant_Projection___('ClientProfileHandling', admin_role_);
   Grant_Projection___('ConfigurationStatusAnalysis', admin_role_);
   Grant_Projection___('DataEntServiceActLogHandling', admin_role_);
   Grant_Projection___('DataSyncProcessSettingsHandling', admin_role_);
   Grant_Projection___('DataSynchronizationStatusHandling', admin_role_);
   Grant_Projection___('DeferralRequestReasonHandling', admin_role_);
   Grant_Projection___('DocumentFileTypesHandling', admin_role_);
   Grant_Projection___('EngineeringUnitsHandling', admin_role_);
   Grant_Projection___('ExternalFileTransactionsHandling', admin_role_);
   Grant_Projection___('ExternalFileLogHandling', admin_role_);
   Grant_Projection___('FailureTypeHandling', admin_role_);
   Grant_Projection___('FaultActionHandling', admin_role_);
   Grant_Projection___('FaultDeferralHandling', admin_role_);
   Grant_Projection___('FaultHandling', admin_role_);
   Grant_Projection___('FaultLabourHandling', admin_role_);
   Grant_Projection___('FaultPartHandling', admin_role_);
   Grant_Projection___('FaultSourceHandling', admin_role_);
   Grant_Projection___('FlightHandling', admin_role_);
   Grant_Projection___('FlmAssemblyFluidDefinitionHandling', admin_role_);
   Grant_Projection___('FlmFluidServiceDefHandling', admin_role_);
   Grant_Projection___('FlmLoadWorkscopeHandling', admin_role_);
   Grant_Projection___('FlmParametersHandling', admin_role_);
   Grant_Projection___('FlmTurnLabourResourceHandling', admin_role_);
   Grant_Projection___('FndSettings', admin_role_);
   Grant_Projection___('FunctionalSettingsHandling', admin_role_);
   Grant_Projection___('GenerateConfigurationScriptAssistant', admin_role_);
   Grant_Projection___('HeadquartersSitesHandling', admin_role_);
   Grant_Projection___('InstallationSettingsHandling', admin_role_);
   Grant_Projection___('KeystoresHandling', admin_role_);
   Grant_Projection___('LogbookTypeHandling', admin_role_);
   Grant_Projection___('MaintLocationTypeHandling', admin_role_);
   Grant_Projection___('MaintenanceLocationHandling', admin_role_);
   Grant_Projection___('MeasurementCategoriesHandling', admin_role_);
   Grant_Projection___('MeasurementTypesHandling', admin_role_);
   Grant_Projection___('MxConfigHandling', admin_role_);
   Grant_Projection___('MyAdministration', admin_role_);
   Grant_Projection___('ObjectPropertiesHandling', admin_role_);
   Grant_Projection___('PermissionSetHandling', admin_role_);
   Grant_Projection___('PhaseOfFlightHandling', admin_role_);
   Grant_Projection___('ProjectionCheckpointHandling', admin_role_);
   Grant_Projection___('RegulatoryBodyHandling', admin_role_);
   Grant_Projection___('RemovalReasonHandling', admin_role_);
   Grant_Projection___('RepositoryHandling', admin_role_);
   Grant_Projection___('RemoteAssistCustomerHandling', admin_role_);
   Grant_Projection___('RuleConfigurationHandling', admin_role_);
   Grant_Projection___('RuleLocationsHandling', admin_role_);
   Grant_Projection___('RuleUsageHandling', admin_role_);
   Grant_Projection___('SatelliteSitesHandling', admin_role_);
   Grant_Projection___('ScheduledDatabaseTaskChainsHandling', admin_role_);
   Grant_Projection___('ScheduledDatabaseTaskChainsHandling', admin_role_);
   Grant_Projection___('ScheduledDatabaseTasksHandling', admin_role_);
   Grant_Projection___('StreamSubscriptions', admin_role_);
   Grant_Projection___('SynchronizationRulesHandling', admin_role_);
   Grant_Projection___('SynchronizeConfigurationsAssistantHandling', admin_role_);
   Grant_Projection___('TaskHandling', admin_role_);
   Grant_Projection___('TaskMeasurementsHandling', admin_role_);
   Grant_Projection___('UserGroupHandling', admin_role_);
   Grant_Projection___('UserHandling', admin_role_);
   Grant_Projection___('UserPinHandling', admin_role_);
   Grant_Projection___('UserSharedSecret', admin_role_);
   Grant_Projection___('WorkPackageDetailsHandling', admin_role_);
   Grant_Projection___('WorkTypeHandling', admin_role_);
   Grant_Projection___('MediaLibraryAttachmentHandling', admin_role_);
   Grant_Projection___('MediaLibraryManagerHandling', admin_role_);
   Grant_Projection___('EventActionHandling', admin_role_);
   Grant_Projection___('AvEsignLogoHandling', admin_role_);
   Grant_Projection___('FlmFluidConsumptionLobbyHandling', admin_role_);
   Grant_Projection___('CompanySiteHandling', admin_role_);
   Grant_Projection___('SitesHandling', admin_role_);
   Grant_Projection___('IdentityAndAccessHandling', admin_role_);
   Grant_Projection___('FlmCriticalItemTypeHandling', admin_role_);
   Grant_Projection___('FlmCriticalItemSeveritiesHandling', admin_role_);
   Grant_Projection___('EventLogAttachmentHandling', admin_role_);
   Grant_Projection___('TaskCountSummaryWidgetHandling', admin_role_);

   --Grant Lobby Page for Admin
   Grant_Lobby_Page___('lobbyPage42f46ace-742f-4186-9e4d-5d730437284b', admin_role_);
   Grant_Lobby_Page___('lobbyPagef36ae1f2-7f6a-4b74-86d1-1adbd7087216', admin_role_);
   Grant_Lobby_Page___('lobbyPage8b4f9361-2f22-40bf-a48f-49b0e4b381d1', admin_role_);
   Grant_Lobby_Page___('lobbyPage60c9811f-595a-4025-a820-69e01c6e31b3', admin_role_);
   Grant_Lobby_Page___('lobbyPagec34b39a9-2a38-4466-9ba5-62f97e013836', admin_role_);
   Grant_Lobby_Page___('lobbyPagec894acb6-caa1-4c76-883f-907712bc7097', admin_role_);
   
   --Grant Security Groups for Admin
   Grant_Security_Groups___('FLMaintApp 1.DocumentManagement', admin_role_);
   Grant_Security_Groups___('FLMaintApp 1.FLMaintApp', admin_role_);
   Grant_Security_Groups___('FLMaintApp 1.MediaLibraryManagement', admin_role_);
   Grant_Security_Groups___('FLMaintApp 1.MobileObjectConnectionConfigManagement', admin_role_);
   Grant_Security_Groups___('FLMaintApp 1.ReplaceMediaLibraryItem', admin_role_);
   
END Do_MM_Admin_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_Line_Planner_Grants___
IS
   planner_role_ CONSTANT VARCHAR2(30) := 'MM_LINE_PLANNER';
BEGIN
   
   Security_SYS.Create_Role(planner_role_,'Access grants for a Line Planner for Mobile Maintenance', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');
   Security_SYS.Clear_Role(planner_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', planner_role_);
   
   --Projection grants for line planner.
   Grant_Projection___('FlmLoadWorkscopeHandling', planner_role_);
   Grant_Projection___('ExternalFileTransactionsHandling', planner_role_);
   Grant_Projection___('ExternalFileLogHandling', planner_role_);
   
END Do_Line_Planner_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_Mm_Flight_Api_Grants___
IS
   flight_api_role_ CONSTANT VARCHAR2(30) := 'MM_FLIGHT_API';
BEGIN
   
   Security_SYS.Create_Role(flight_api_role_,'Access grants for Mobile Maintenance open API for flights', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');
   Security_SYS.Clear_Role(flight_api_role_);
   
   --Projection grants for flight API user.
   Grant_Projection___('FlightHandling', flight_api_role_);
   
END Do_Mm_Flight_Api_Grants___;

--override_hard_stop_role_
@IgnoreUnitTest NoOutParams
PROCEDURE Do_Mm_Override_Grants___
IS
   role_desc_   VARCHAR2(200) := 'Access grants to release an aircraft overriding a hard stop for missing mandatory components and overdue maintenance';
BEGIN
   IF (Fnd_Role_Api.Get(override_hard_stop_role_).fnd_role_type IS NULL) THEN
      Security_SYS.Create_Role(override_hard_stop_role_, role_desc_, 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');
   ELSE
      Security_SYS.Clear_Role(override_hard_stop_role_);
   END IF;
   
   --granting roles
   Grant_Role___('FND_DSS_ASST_ENDUSER', override_hard_stop_role_);
   Grant_Role___('FND_MOBILE_APP_SYNC_TRACE', override_hard_stop_role_);
   Grant_Role___('FND_REM_ASST_ENDUSER', override_hard_stop_role_);
   Grant_Role___('FND_WEBENDUSER_MAIN', override_hard_stop_role_);
   Grant_Role___('MOBILE_APP_RUNTIME', override_hard_stop_role_);
 
   --granting projections
   Grant_Projection___('FLMaintApp', override_hard_stop_role_);
   Grant_Projection___('FlmAircraftTurnsDetailsHandling', override_hard_stop_role_);
   Grant_Projection___('FlmAircraftTurnsNavigatorEntry', override_hard_stop_role_);   
   Grant_Projection___('FlmMyAircraftTurnsHandling', override_hard_stop_role_);
   
   --granting security groups
   Grant_Security_Groups___('FLMaintApp 1.FLMaintApp', override_hard_stop_role_);
   Grant_Security_Groups___('FLMaintApp 1.DocumentManagement', override_hard_stop_role_);
END Do_Mm_Override_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_Hangar_Technician_Grants___
IS
BEGIN
   
   Security_SYS.Create_Role(hangar_technician_role_, 'Access grants for the Hangar Technician under the Mobile Maintenance Solution', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');  
   Security_SYS.Clear_Role(hangar_technician_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', hangar_technician_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD', hangar_technician_role_);
   Grant_Role___('FND_DSS_ASST_ENDUSER', hangar_technician_role_);
   
   --Projections for Hangar Technician.
   Grant_Projection___('AdcomNavigator', hangar_technician_role_);
   Grant_Projection___('FlmexeNavigator', hangar_technician_role_);
   Grant_Projection___('FlmFaultDetailHandling', hangar_technician_role_);
   Grant_Projection___('FlmTaskDetailHandling', hangar_technician_role_);
   Grant_Projection___('FlmHangarTechnicianLobbyHandling', hangar_technician_role_);
   Grant_Projection___('FlmNonRoutinesHandling', hangar_technician_role_);
   Grant_Projection___('FlmNonRoutinesOfWorkPackageHandling', hangar_technician_role_);
   Grant_Projection___('FlmHmTechnicianTaskAssignmentsHandling', hangar_technician_role_);
   Grant_Projection___('FlmHmTechnicianMyAssignmentsHandling', hangar_technician_role_);
   Grant_Projection___('MediaLibraryAttachmentHandling', hangar_technician_role_);
   Grant_Projection___('FlmFaultSearchHandling', hangar_technician_role_);
   Grant_Projection___('MxFaultDetailHandling', hangar_technician_role_);
   Grant_Projection___('FlmHmWorkPackageHandling', hangar_technician_role_);
   Grant_Projection___('MxPartDefinitionSearchHandling', hangar_technician_role_);
   Grant_Projection___('MxInventorytSearchHandling', hangar_technician_role_);
   Grant_Projection___('InventoryPartInStockHandling', hangar_technician_role_);
   Grant_Projection___('FlmHmPreviewReleaseHandling', hangar_technician_role_);
   Grant_Projection___('FlmMyPartRequestHandling', hangar_technician_role_);
   Grant_Projection___('FlmPartTagReportArchiveHandling', hangar_technician_role_);
   Grant_Projection___('ServiceableTagRep', hangar_technician_role_);
   Grant_Projection___('UnserviceableTagRep', hangar_technician_role_);
   Grant_Projection___('QuarantineTagRep', hangar_technician_role_);
   Grant_Projection___('EventLogAttachmentHandling', hangar_technician_role_);
      
   --Grant madatory projections are required for using Maintenix integration 
   Grant_Read_Only_Projection___('AdmonNavigator', hangar_technician_role_);
   Grant_Read_Only_Projection___('MxZoneDetailsHandling', hangar_technician_role_);
   Grant_Read_Only_Projection___('MxPanelDetailsHandling', hangar_technician_role_);
   Grant_Read_Only_Projection___('MxTaskDetailsHandling', hangar_technician_role_);
   Grant_Read_Only_Projection___('MxOpenFaultDetailsHandling', hangar_technician_role_);
   Grant_Read_Only_Projection___('MxInventoryDetailsHandling', hangar_technician_role_);
   Grant_Read_Only_Projection___('MxAircraftDetailsHandling', hangar_technician_role_);
   
   --Grant Lobby Pages for Hangar Technician.
   Grant_Lobby_Page___('lobbyPage8b4f9361-2f22-40bf-a48f-49b0e4b381d1', hangar_technician_role_);
   Grant_Lobby_Page___('lobbyPage60c9811f-595a-4025-a820-69e01c6e31b3', hangar_technician_role_);
     
   -- revoke unwanted actions
   Fnd_Proj_Action_Grant_API.Do_Revoke('FlmHmWorkPackageHandling', 'UpdateSelectedTaskContract', hangar_technician_role_); 
   Fnd_Proj_Entity_Grant_API.Revoke_CUD('FlmHmWorkPackageHandling', 'AvAircraftWorkPackage', hangar_technician_role_);
   Fnd_Proj_Entity_Grant_API.Revoke_CUD('FlmHmWorkPackageHandling', 'AvExeTask', hangar_technician_role_);
   
   -- Grant actions
   Fnd_Proj_Action_Grant_API.Do_Grant('FlmHmWorkPackageHandling', 'DeleteWpSignOffSkill', hangar_technician_role_);
  
END Do_Hangar_Technician_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_Hangar_Supervisor_Grants___
IS
BEGIN
   
   Security_SYS.Create_Role(hangar_supervisor_role_, 'Access grants for the Hangar Supervisor under the Base Maintenance Solution', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');  
   Security_SYS.Clear_Role(hangar_supervisor_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', hangar_supervisor_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD', hangar_supervisor_role_);
   Grant_Role___('FND_DSS_ASST_ENDUSER', hangar_supervisor_role_);
   
   --Projections for Hangar Supervisor.
   Grant_Projection___('AdcomNavigator', hangar_supervisor_role_);
   Grant_Projection___('FlmexeNavigator', hangar_supervisor_role_);
   Grant_Projection___('FlmFaultDetailHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmTaskDetailHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmHmSupervisorAirportLobbyHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmHmSupervisorWPLobbyHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmNonRoutinesHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmNonRoutinesOfWorkPackageHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmHmCrewLeadTasksHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmHmWorkPackageHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmHmSupervisorMyShiftBoardHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmFaultSearchHandling', hangar_supervisor_role_);
   Grant_Projection___('MxFaultDetailHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmCriticalItemTypeHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmCriticalItemSeveritiesHandling', hangar_supervisor_role_);
   Grant_Projection___('HMShiftHandoverReportRep', hangar_supervisor_role_);
   Grant_Projection___('MxPartDefinitionSearchHandling', hangar_supervisor_role_);
   Grant_Projection___('MxInventorytSearchHandling', hangar_supervisor_role_);
   Grant_Projection___('InventoryPartInStockHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmHmPreviewReleaseHandling', hangar_supervisor_role_);
   Grant_Projection___('EventLogAttachmentHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmMyPartRequestHandling', hangar_supervisor_role_);
   Grant_Projection___('TaskCountSummaryWidgetHandling', hangar_supervisor_role_);
   Grant_Projection___('FlmPartTagReportArchiveHandling', hangar_supervisor_role_);
   Grant_Projection___('ServiceableTagRep', hangar_supervisor_role_);
   Grant_Projection___('UnserviceableTagRep', hangar_supervisor_role_);
   Grant_Projection___('QuarantineTagRep', hangar_supervisor_role_);
   Grant_Projection___('EventLogAttachmentHandling', hangar_supervisor_role_);

   --Grant madatory projections are required for using Maintenix integration 
   Grant_Read_Only_Projection___('AdmonNavigator', hangar_supervisor_role_);
   
   Grant_Read_Only_Projection___('CustomersHandling', hangar_supervisor_role_);
   Grant_Read_Only_Projection___('MxZoneDetailsHandling', hangar_supervisor_role_);
   Grant_Read_Only_Projection___('MxPanelDetailsHandling', hangar_supervisor_role_);
   Grant_Read_Only_Projection___('MxTaskDetailsHandling', hangar_supervisor_role_);
   Grant_Read_Only_Projection___('MxOpenFaultDetailsHandling', hangar_supervisor_role_);
   Grant_Read_Only_Projection___('MxInventoryDetailsHandling', hangar_supervisor_role_);
   Grant_Read_Only_Projection___('MxAircraftDetailsHandling', hangar_supervisor_role_);
   
   --Grant Lobby Pages for Hangar Supervisor.
   Grant_Lobby_Page___('lobbyPagec34b39a9-2a38-4466-9ba5-62f97e013836', hangar_supervisor_role_);
   Grant_Lobby_Page___('lobbyPagec894acb6-caa1-4c76-883f-907712bc7097', hangar_supervisor_role_);
     
   -- revoke unwanted actions
   Fnd_Proj_Action_Grant_API.Do_Revoke('FlmHmWorkPackageHandling', 'UpdateSelectedTaskContract', hangar_supervisor_role_); 
   Fnd_Proj_Entity_Grant_API.Revoke_CUD('FlmHmWorkPackageHandling', 'AvAircraftWorkPackage', hangar_supervisor_role_);
   Fnd_Proj_Entity_Grant_API.Revoke_CUD('FlmHmWorkPackageHandling', 'AvExeTask', hangar_supervisor_role_);
   
   -- Grant actions
   Fnd_Proj_Action_Grant_API.Do_Grant('FlmHmWorkPackageHandling', 'DeleteWpSignOffSkill', hangar_supervisor_role_);

END Do_Hangar_Supervisor_Grants___;

@IgnoreUnitTest NoOutParams
PROCEDURE Do_Hangar_Crew_Lead_Grants___
IS
BEGIN
   
   Security_SYS.Create_Role(hangar_crew_lead_role_, 'Access grants for the Hangar Crew Lead under the Base Maintenance Solution', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');  
   Security_SYS.Clear_Role(hangar_crew_lead_role_);
   
   Grant_Role___('FND_WEBENDUSER_MAIN', hangar_crew_lead_role_);
   Grant_Role___('DOCUMENT_ATTACHMENT_CLOUD', hangar_crew_lead_role_);
   Grant_Role___('FND_DSS_ASST_ENDUSER', hangar_crew_lead_role_);
   
   --Projections for Hangar Crew Lead.
   Grant_Projection___('AdcomNavigator', hangar_crew_lead_role_);
   Grant_Projection___('FlmexeNavigator', hangar_crew_lead_role_);
   Grant_Projection___('FlmFaultDetailHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmTaskDetailHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmHmCrewLeadLobbyHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmHmWorkPackageHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmNonRoutinesHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmNonRoutinesOfWorkPackageHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmHmCrewLeadTasksHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmHmTechnicianMyAssignmentsHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmFaultSearchHandling', hangar_crew_lead_role_);
   Grant_Projection___('MxFaultDetailHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmCriticalItemTypeHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmCriticalItemSeveritiesHandling', hangar_crew_lead_role_);
   Grant_Projection___('HMShiftHandoverReportRep', hangar_crew_lead_role_);
   Grant_Projection___('MxPartDefinitionSearchHandling', hangar_crew_lead_role_);
   Grant_Projection___('MxInventorytSearchHandling', hangar_crew_lead_role_);
   Grant_Projection___('InventoryPartInStockHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmHmPreviewReleaseHandling', hangar_crew_lead_role_);
   Grant_Projection___('EventLogAttachmentHandling', hangar_crew_lead_role_);
   Grant_Projection___('FlmMyPartRequestHandling', hangar_crew_lead_role_);
   Grant_Projection___('TaskCountSummaryWidgetHandling', hangar_crew_lead_role_);
   Grant_Projection___('EventLogAttachmentHandling', hangar_crew_lead_role_);
   
   --Grant madatory projections are required for using Maintenix integration 
   Grant_Read_Only_Projection___('AdmonNavigator', hangar_crew_lead_role_);
   Grant_Read_Only_Projection___('MxPanelDetailsHandling', hangar_crew_lead_role_);
   Grant_Read_Only_Projection___('MxZoneDetailsHandling', hangar_crew_lead_role_);
   Grant_Read_Only_Projection___('MxTaskDetailsHandling', hangar_crew_lead_role_);
   Grant_Read_Only_Projection___('MxOpenFaultDetailsHandling', hangar_crew_lead_role_);
   Grant_Read_Only_Projection___('MxInventoryDetailsHandling', hangar_crew_lead_role_);
   Grant_Read_Only_Projection___('MxAircraftDetailsHandling', hangar_crew_lead_role_);
   
   --Grant Lobby Pages for Hangar Supervisor.
   Grant_Lobby_Page___('lobbyPage0a9a3fdf-b5e3-4325-ab78-09f1c6ff00e5', hangar_crew_lead_role_);
   Grant_Lobby_Page___('lobbyPage825ea048-87c2-455f-807e-ed6ef203631d', hangar_crew_lead_role_);
     
   -- revoke unwanted actions
   Fnd_Proj_Action_Grant_API.Do_Revoke('FlmHmWorkPackageHandling', 'UpdateSelectedTaskContract', hangar_crew_lead_role_); 
   Fnd_Proj_Entity_Grant_API.Revoke_CUD('FlmHmWorkPackageHandling', 'AvAircraftWorkPackage', hangar_crew_lead_role_);
   Fnd_Proj_Entity_Grant_API.Revoke_CUD('FlmHmWorkPackageHandling', 'AvExeTask', hangar_crew_lead_role_);
   
   -- Grant actions
   Fnd_Proj_Action_Grant_API.Do_Grant('FlmHmWorkPackageHandling', 'DeleteWpSignOffSkill', hangar_crew_lead_role_);

END Do_Hangar_Crew_Lead_Grants___;

-------------------- LU SPECIFIC PRIVATE METHODS ----------------------------


-------------------- LU SPECIFIC PROTECTED METHODS --------------------------


-------------------- LU SPECIFIC PUBLIC METHODS -----------------------------
--SAFE_FOR_ONLINE_DEPLOYMENT(2025-09-12, KAPALK, EDITION_STRATERGY_USED)
@IgnoreUnitTest NoOutParams
PROCEDURE Post_Installation_Object
IS   
BEGIN
   Security_SYS.Create_Role(role_, 'Role for Mobile Maintenance Supervisor', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');  
END Post_Installation_Object;

--SAFE_FOR_ONLINE_DEPLOYMENT(2025-08-01, KAPALK, EDITION_STRATERGY_USED)
@IgnoreUnitTest NoOutParams
PROCEDURE Post_Installation_Data 
IS
BEGIN   
   IF Installation_SYS.Get_Installation_Mode = FALSE OR Module_API.Is_Included_In_Delivery('FLMEXE') THEN
      IF Database_SYS.Component_Active('FLMEXE') THEN
         -- grant flm supervisor related projections.
         Security_SYS.Grant_Projection('FlmSupervisorAircraftTurnsDetailsHandling', role_);
         Security_SYS.Grant_Projection('FlmAircraftTurnsDetailsHandling', role_);
         Security_SYS.Grant_Projection('FlmStationTurnsHandling', role_);
         Security_SYS.Grant_Projection('FlmAircraftTurnsDetailsHandling', role_);
         Security_SYS.Grant_Projection('FlmMyAircraftTurnsHandling', role_);
         Security_SYS.Grant_Projection('FlmTaskWorkAssignmentHandling', role_);
         Security_SYS.Grant_Projection('FlmFaultDetailHandling', role_);
         Security_SYS.Grant_Projection('FlmMyWorksHandling', role_);
         Security_SYS.Grant_Projection('FlmTaskDetailHandling', role_);
         Security_SYS.Grant_Projection('FlmTurnLabourResourceHandling', role_);
         Security_SYS.Grant_Projection('FlmParametersHandling', role_);
         Security_SYS.Grant_Projection('FlmAircraftTurnsNavigatorEntry', role_);
         Security_SYS.Grant_Projection('FlmTechnicianLobbyHandling', role_);
         Security_SYS.Grant_Projection('FlmLineWorkManagementLobbyHandling', role_);
         Security_SYS.Grant_Projection('LMShiftHandoverReportRep', role_);
         Security_SYS.Grant_Projection('MxPartDefinitionSearchHandling', role_);
         Security_SYS.Grant_Projection('MxInventorytSearchHandling', role_); 
         Security_SYS.Grant_Projection('InventoryPartInStockHandling', role_); 
         Security_SYS.Grant_Projection('ManualIssueAssistantHandling', role_);
         Security_SYS.Grant_Projection('FlmPartTagReportArchiveHandling', role_);
         Security_SYS.Grant_Projection('ServiceableTagRep', role_);
         Security_SYS.Grant_Projection('UnserviceableTagRep', role_);
         Security_SYS.Grant_Projection('QuarantineTagRep', role_);
         Security_SYS.Grant_Pres_Object('lobbyPaged222b6cd-42e3-4f77-8b06-a891a635b6d4', role_);  
         Security_SYS.Grant_Pres_Object('lobbyPage32800a3e-6d9a-40a6-8ed5-d71f510ada05', role_);
         Security_SYS.Grant_Pres_Object('MxWorkPackageDetailsHandling', role_);
         Security_SYS.Grant_Pres_Object('FlmTaskCardHandling', role_);
         
         -- revoke unwanted actions
         Fnd_Proj_Action_Grant_API.Do_Revoke('FlmAircraftTurnsDetailsHandling', 'ClearReleaseAircraftVirtual', role_);
         Fnd_Proj_Ent_Action_Grant_API.Do_Revoke('FlmTaskDetailHandling','AvExeTask','Start',role_);
         Fnd_Proj_Ent_Action_Grant_API.Do_Revoke('FlmAircraftTurnsDetailsHandling','AvExeTask','Start',role_);
         Fnd_Proj_Action_Grant_API.Do_Revoke('FlmTaskDetailHandling', 'ClearFaultDefMainVirtual', role_);
         Fnd_Proj_Action_Grant_API.Do_Revoke('FlmTaskDetailHandling', 'Sign', role_);
         
         -- grant read only permission for MM supervisor
         Grant_Read_Only_Projection___('MxZoneDetailsHandling', role_);
         Grant_Read_Only_Projection___('MxPanelDetailsHandling', role_);
         
         -- grant other roles
         Security_SYS.Grant_Role('FND_WEBENDUSER_MAIN', role_);
         
         Do_Line_Technician_Grants___;
         
         -- grant permission for MOC
         Do_MOC_Grants___;
         
         -- grant permission for MM Admin
         Do_MM_Admin_Grants___;
         
         -- grant permission for Line Planner
         Do_Line_Planner_Grants___;
         
         -- grant permission for flight API user
         Do_Mm_Flight_Api_Grants___;
         
         -- grant permission for MM Override Hard Stop
         Do_Mm_Override_Grants___;
         
         -- grant permission for Hangar Technician
         Do_Hangar_Technician_Grants___;
          
         -- grant permission for Hangar Supervisor
         Do_Hangar_Supervisor_Grants___;
         
         -- grant permission for Hangar Crew Lead
         Do_Hangar_Crew_Lead_Grants___;
         
      END IF;
   END IF; 
END Post_Installation_Data;

-------------------- LU  NEW METHODS -------------------------------------
