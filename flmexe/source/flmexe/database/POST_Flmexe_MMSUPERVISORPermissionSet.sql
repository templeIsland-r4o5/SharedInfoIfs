-----------------------------------------------------------------------------
--  Module : FLMEXE
--
--  File   : POST_Flmexe_MMSUPERVISORPermissionSet.sql
--
--  IFS Developer Studio Template Version 2.6
--
--  Date     Sign    History
--  ------   ------  --------------------------------------------------
--  240418   ROERLK  AD-12569, Granted FlmLineWorkManagementLobbyHandling projection to MM_SUPERVISOR
--  240417   WAISLK  AD-12567, Granted FlmTechnicianLobbyHandling projection to MM_SUPERVISOR.
--  240214   majslk  AD-12145, Modified MM_SUPERVISOR permission set with IFS_MANAGED delivery type
--  230925   Satglk  AD-10779, Granted Technician Lobby to Supervisor.
--  230214   vaallk  Created
--  ------   ------  --------------------------------------------------
-----------------------------------------------------------------------------

SET SERVEROUTPUT ON

exec Database_SYS.Log_Detail_Time_Stamp('FLMEXE','POST_Flmexe_MMSUPERVISORPermissionSet.sql','Timestamp_1');
PROMPT Remove obsolete permission set FLM_SUPERVISOR in FLM
--SAFE_FOR_ONLINE_DEPLOYMENT(2025-08-01, KAPALK, EDITION_STRATERGY_USED)
DECLARE
   role_ VARCHAR2(30) := 'FLM_SUPERVISOR';
BEGIN
   Edition_Strategy_SYS.Enable_Edition_Strategy_Grants;
   IF Fnd_Role_API.Exists(role_) THEN
      Security_SYS.Clear_Role(role_);
      Security_SYS.Drop_Role(role_);
   END IF;
END;
/

COMMIT;

exec Database_SYS.Log_Detail_Time_Stamp('FLMEXE','POST_Flmexe_MMSUPERVISORPermissionSet.sql','Timestamp_2');
PROMPT new permission SET MM_SUPERVISOR IN FLM
--SAFE_FOR_ONLINE_DEPLOYMENT(2025-08-01, KAPALK, EDITION_STRATERGY_USED)
DECLARE
   role_ VARCHAR2(30) := 'MM_SUPERVISOR';
BEGIN
   Edition_Strategy_SYS.Enable_Edition_Strategy_Grants;
   IF Fnd_Role_API.Exists(role_) = FALSE THEN
      Security_SYS.Create_Role(role_, 'Role for Mobile Maintenance Supervisor', 'ENDUSERROLE', 'TRUE', 'IFS_MANAGED');  
      IF Installation_SYS.Get_Installation_Mode = FALSE OR Module_API.Is_Included_In_Delivery('FLMEXE') THEN
         IF Database_SYS.Component_Active('FLMEXE') THEN
            -- grant flm supervisor related projections
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
            Security_SYS.Grant_Projection('FlmTechnicianLobbyHandling', role_);
            Security_SYS.Grant_Projection('FlmLineWorkManagementLobbyHandling', role_);
            Security_SYS.Grant_Pres_Object('lobbyPaged222b6cd-42e3-4f77-8b06-a891a635b6d4', role_);  
            Security_SYS.Grant_Pres_Object('lobbyPage32800a3e-6d9a-40a6-8ed5-d71f510ada05', role_);
            Security_SYS.Grant_Projection('FlmMyPartRequestHandling', role_);

            -- revoke unwanted actions
            Fnd_Proj_Action_Grant_API.Do_Revoke('FlmAircraftTurnsDetailsHandling', 'ClearReleaseAircraftVirtual', role_);
            Fnd_Proj_Ent_Action_Grant_API.Do_Revoke('FlmTaskDetailHandling','AvExeTask','Start',role_);
            Fnd_Proj_Ent_Action_Grant_API.Do_Revoke('FlmAircraftTurnsDetailsHandling','AvExeTask','Start',role_);
            Fnd_Proj_Action_Grant_API.Do_Revoke('FlmTaskDetailHandling', 'ClearFaultDefMainVirtual', role_);
            Fnd_Proj_Action_Grant_API.Do_Revoke('FlmTaskDetailHandling', 'Sign', role_);

            -- grant other roles
            Security_SYS.Grant_Role('FND_WEBENDUSER_MAIN', role_);
         END IF;
      END IF; 
   END IF;
END;
/

COMMIT;

exec Database_SYS.Log_Detail_Time_Stamp('FLMEXE','POST_Flmexe_MMSUPERVISORPermissionSet.sql','Timestamp_3');
PROMPT DROP FlmMocAircraftTurnsNavigatorEntry Client AND Projection
--SAFE_FOR_ONLINE_DEPLOYMENT(2025-08-01, KAPALK, EDITION_STRATERGY_USED)
DECLARE
BEGIN
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJECTION_USAGE_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_ACTION_USAGE_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_ENT_ACTION_USAGE_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_VIRTUAL_ENTITY_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_JAVA_IMPLEMENTATIONS_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_LARGE_ATTR_SUPP_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJECTION_GRANT_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_ENTITY_GRANT_TAB');  
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_ACTION_GRANT_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJ_ENT_ACTION_GRANT_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('DATA_ENT_SERVICE_ACT_LOG_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('DATA_ENT_SERVICE_SETTING_TAB');
   Edition_Strategy_SYS.Enable_Edition_Strategy('FND_PROJECTION_TAB');
   Database_SYS.Remove_Client('FlmMocAircraftTurnsNavigatorEntry');
   Database_SYS.Remove_Projection('FlmMocAircraftTurnsNavigatorEntry');
END;
/

COMMIT;
exec Database_SYS.Log_Detail_Time_Stamp('FLMEXE','POST_Flmexe_MMSUPERVISORPermissionSet.sql','Done');


