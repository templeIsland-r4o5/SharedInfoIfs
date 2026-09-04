-----------------------------------------------------------------------------
--
--  Logical unit: FlmexeUtil
--  Component:    FLMEXE
--
--  IFS Developer Studio Template Version 3.0
--
--  Date    Sign    History
--  ------  ------  ---------------------------------------------------------
--  250502  VAALLK  AD-18257, Added Is_Hangar_Planner 
--  240217  ROERLK  AD-17035, Added function Get_Fault_Maint_Location_T_Z 
--  241017  WEDILK  AD-14537, Change to use av_exe_task/jt_task_tab after changing AvExeTask with based on JtTask
--  240130  DUWJLK  AD-10942, Modified Show_Defer_Warning method message content.
--  240117  majslk  AD-10940, Implemented Show_Defer_Warning method
--  240104  PSUALK  AD-11816, Task/Turn Assignment duration can enter less than 1 hr.
--  221122  SUPKLK  AD-8948, Updated Get_User_Roles method to return all the permissions concated.
--  221114  SUPKLK  AD-8948, Added Get_User_Role method.
--  221102  ROSDLK  AD-8697, Added Is_Moc_Role_Exists method.
-----------------------------------------------------------------------------

layer Core;

-------------------- PUBLIC DECLARATIONS ------------------------------------


-------------------- PRIVATE DECLARATIONS -----------------------------------


-------------------- LU SPECIFIC IMPLEMENTATION METHODS ---------------------


-------------------- LU SPECIFIC PRIVATE METHODS ----------------------------


-------------------- LU SPECIFIC PROTECTED METHODS --------------------------


-------------------- LU SPECIFIC PUBLIC METHODS -----------------------------

@UncheckedAccess
FUNCTION Is_MOC_Role_Exists (
   identity_ IN VARCHAR2 ) RETURN VARCHAR2
IS
   user_role_ VARCHAR2(30) := 'MM_MAINT_OPERATIONS_CONTROLLER';
   
   CURSOR get_user_roles IS
      SELECT role
      FROM   fnd_user_role_tab
      WHERE  identity = identity_; 
BEGIN
   FOR rec IN get_user_roles LOOP
      IF rec.role = user_role_ THEN
         RETURN 'TRUE';
      END IF;
   END LOOP;
   RETURN 'FALSE';
END Is_MOC_Role_Exists;

@UncheckedAccess
FUNCTION Get_User_Roles (
   identity_ IN VARCHAR2 ) RETURN VARCHAR2
IS
   tech_role_ VARCHAR2(30) := 'MM_TECHNICIAN';
   moc_role_ VARCHAR2(30) := 'MM_MAINT_OPERATIONS_CONTROLLER';
   sup_role_ VARCHAR2(30) := 'MM_SUPERVISOR';
   role_cont_  VARCHAR2(4000);
   
   CURSOR get_user_roles IS
      SELECT role
      FROM   fnd_user_role_tab
      WHERE  identity = identity_ AND role IN (tech_role_,moc_role_,sup_role_)
      ORDER BY role asc; 
BEGIN
   FOR rec IN get_user_roles LOOP
      IF role_cont_ IS NULL THEN
         role_cont_ := rec.role;
      ELSE
         role_cont_ := role_cont_ || '^' || rec.role;
      END IF;
   END LOOP;
   RETURN role_cont_;
END Get_User_Roles;

FUNCTION Validate_Duration(
   duration_hhmm_ IN VARCHAR2) RETURN BOOLEAN
IS
BEGIN
   IF(duration_hhmm_ IS NULL OR LENGTH(TRIM(duration_hhmm_))=0) THEN
      RETURN TRUE;
   ELSE 
      IF(INSTR(duration_hhmm_, ':') != 0) THEN
         IF(INSTR(duration_hhmm_,':')+2 = LENGTH(duration_hhmm_)) THEN
            IF(LENGTH(TRIM(TRANSLATE(SUBSTR(duration_hhmm_,1,INSTR(duration_hhmm_,':')-1), '0123456789',' '))) IS NULL) AND (LENGTH(TRIM(TRANSLATE(SUBSTR(duration_hhmm_,INSTR(duration_hhmm_,':')+1,LENGTH(duration_hhmm_)), '0123456789',' '))) IS NULL) THEN
               RETURN TRUE;
            ELSE
               RETURN FALSE;
            END IF;
         ELSE
            RETURN FALSE;
         END IF;
      ELSE
         RETURN FALSE;
      END IF;
   END IF;
END Validate_Duration;

FUNCTION Show_Defer_Warning (
   task_seq_ IN NUMBER,
   aircraft_wp_id_ IN NUMBER) RETURN VARCHAR2
IS
   TYPE config_slot_array IS TABLE OF VARCHAR2(50) INDEX BY VARCHAR2(50);
   config_slot_array_            config_slot_array;
   
   removed_conf_slot_code_       av_config_slot_position_tab.config_slot_code%TYPE;
   removal_count_in_task_        NUMBER; 
   install_count_in_task_        NUMBER; 
   removal_count_                NUMBER; 
   install_count_                NUMBER; 
   config_slots_                 VARCHAR2(3000):= NULL;
   arr_index_                    NUMBER:= 1;
   warning_message_              VARCHAR2(3000):= NULL;
   item_exist_                   BOOLEAN:= FALSE;
   
   -- fetch all the signed part removals of the task
   CURSOR get_signed_part_removals IS
      SELECT 
         * 
      FROM  
         av_exe_task_part_tab tp
      INNER JOIN av_part_group_part_tab pgp ON
         pgp.part_no_id = tp.removed_part_no_id  AND
         pgp.part_group_id = tp.part_group_id 
      INNER JOIN av_part_group_tab pg ON
         pg.part_group_id = pgp.part_group_id 
      LEFT JOIN av_config_slot_tab cs ON 
         cs.config_slot_code = pg.config_slot_code AND    
         cs.assembly_type_code = pg.assembly_type_code 
      WHERE 
         tp.task_seq = task_seq_ and tp.removed_user IS NOT NULL AND
         cs.is_mandatory = 'TRUE' AND
         pg.inventory_class_code IN ('ASSY', 'TRK');
      
   -- fetch all the signed removals and signed installtions with same config slot position and  
   -- same assembly config slot position inside the task and find matching installations.
   CURSOR get_signed_task_part_rec(config_slot_position_id_ NUMBER, assmbly_config_slot_pos_id_ NUMBER, task_seq_ NUMBER) IS
      SELECT 
         * 
      FROM  
         av_exe_task_part_tab tp
      WHERE 
         tp.task_seq = task_seq_ AND 
         tp.config_slot_position_id = config_slot_position_id_ AND
         ((tp.assmbly_config_slot_pos_id IS NOT NULL AND tp.assmbly_config_slot_pos_id = assmbly_config_slot_pos_id_) OR (tp.assmbly_config_slot_pos_id IS NULL AND assmbly_config_slot_pos_id_ IS NULL)) AND
         (tp.removed_user IS NOT NULL OR tp.installed_user IS NOT NULL);
   
   -- fetch all the tasks in work paackage       
   CURSOR get_all_tasks_in_wp IS
      SELECT 
         t.task_seq
      FROM 
         av_exe_task t
      WHERE 
         t.aircraft_wp_id = aircraft_wp_id_;
   
BEGIN
   config_slot_array_ := config_slot_array();
   
   -- fetch all the signed part removals of the task
   FOR signed_part_removal_rec_ IN get_signed_part_removals LOOP
      removal_count_in_task_  := 0; 
      install_count_in_task_  := 0; 
      removal_count_          := 0; 
      install_count_          := 0; 
      item_exist_             := FALSE;
      removed_conf_slot_code_ := av_config_slot_position_API.Get_Config_Slot_Code(signed_part_removal_rec_.config_slot_position_id);
         
      -- fetch all the signed removals and signed installtions with same config slot position and  
      -- same assembly config slot position inside the task and find matching installations.      
      FOR signed_task_part_rec_ IN get_signed_task_part_rec (signed_part_removal_rec_.config_slot_position_id, signed_part_removal_rec_.assmbly_config_slot_pos_id, task_seq_) LOOP
         IF signed_task_part_rec_.removed_user IS NOT NULL THEN
            removal_count_in_task_ := removal_count_in_task_ + 1;
         END IF;
         IF signed_task_part_rec_.installed_user IS NOT NULL THEN
            install_count_in_task_ := install_count_in_task_ + 1;
         END IF;
      END LOOP;

      --if no matching installations are found inside the task then find them inside the work package
      IF removal_count_in_task_ > install_count_in_task_ THEN
         FOR task_rec_ IN get_all_tasks_in_wp LOOP
            FOR signed_task_part_rec_ IN get_signed_task_part_rec (signed_part_removal_rec_.config_slot_position_id, signed_part_removal_rec_.assmbly_config_slot_pos_id, task_rec_.task_seq) LOOP
               IF signed_task_part_rec_.removed_user IS NOT NULL THEN
                  removal_count_ := removal_count_ + 1;
               END IF;
               IF signed_task_part_rec_.installed_user IS NOT NULL THEN
                  install_count_ := install_count_ + 1;
               END IF;
            END LOOP;
         END LOOP;         
      END IF;

      --if no matching installations are found inside the work package then store the config slot code inside a list.
      IF removal_count_ > install_count_ THEN
         IF config_slot_array_.COUNT > 0 THEN
            FOR key IN 1..config_slot_array_.COUNT LOOP
               IF config_slot_array_(key) = removed_conf_slot_code_ THEN
                  item_exist_ := TRUE;
                  EXIT; -- Value found, exit the loop
               END IF;
            END LOOP;

            IF NOT item_exist_ THEN
               config_slot_array_(arr_index_) := removed_conf_slot_code_;
               arr_index_ := arr_index_ + 1;            
            END IF;
         ELSE
            config_slot_array_(arr_index_) := removed_conf_slot_code_;
            arr_index_ := arr_index_ + 1;  
         END IF;
      END IF;
                        
   END LOOP;

   IF config_slot_array_.COUNT > 0 THEN
      FOR i IN 1..config_slot_array_.COUNT LOOP
         config_slots_ := config_slots_ || config_slot_array_(i);

         --Adding comma if not the last element
         IF i < config_slot_array_.COUNT THEN
            config_slots_ := config_slots_ || ', ';         
         END IF;
      END LOOP;
   END IF;
   
   IF config_slots_ IS NOT NULL THEN
      warning_message_ :=config_slots_ ;
   END IF;
   
   RETURN warning_message_;
END Show_Defer_Warning;

@IgnoreUnitTest TrivialFunction
FUNCTION Get_Assignment_Status_Filter (
   labor_assigned_to_ IN VARCHAR2) RETURN VARCHAR2
IS
   session_user_                 VARCHAR2(100);
BEGIN
   session_user_ := Fnd_Session_API.Get_Fnd_User;
   
   IF session_user_ = labor_assigned_to_ THEN
      RETURN 'ASSIGN_TO_ME';
   ELSIF (session_user_ != labor_assigned_to_) AND (labor_assigned_to_ IS NOT NULL) THEN
      RETURN 'ASSIGN_TO_OTHERS';
   ELSE 
      RETURN 'UNASSIGNED';
   END IF;
END Get_Assignment_Status_Filter;

@IgnoreUnitTest PipelinedFunction
FUNCTION Get_Shift_By_Sched_Start(
   sched_start_               IN    TIMESTAMP,
   execution_instance_status_ IN    VARCHAR2)
   RETURN    VARCHAR2
IS
   current_user_                 VARCHAR2(30);
   res_seq_                      NUMBER;
   current_date_                 TIMESTAMP := SYSDATE;
   current_shift_start_time_     TIMESTAMP;
   current_shift_finish_time_    TIMESTAMP;
   next_shift_start_time_        TIMESTAMP;
   next_shift_finish_time_       TIMESTAMP;
   shift_                        VARCHAR2(30);
   shift_count_                  NUMBER;
   
   CURSOR Get_All_Shifts IS
   SELECT start_time, finish_time
   FROM resource_capacity_tab
   WHERE resource_seq = res_seq_;
   
   CURSOR Get_Shift_Count IS
   SELECT COUNT(*)
   FROM resource_capacity_tab
   WHERE resource_seq = res_seq_;
   
BEGIN
   current_user_ := Fnd_Session_API.Get_Fnd_User();
   res_seq_ := Resource_API.Get_Resource_Seq(current_user_, Resource_Types_API.DB_PERSON);
   
   OPEN Get_Shift_Count;
   FETCH Get_Shift_Count INTO shift_count_;
   CLOSE Get_Shift_Count;
   
   IF(shift_count_ != 0) THEN
      Resource_Capacity_API.Get_Period_Start_End(current_shift_start_time_, current_shift_finish_time_, res_seq_, current_date_);
      Resource_Capacity_API.Get_Next_Period_Start_End(next_shift_start_time_, next_shift_finish_time_, res_seq_, current_date_);
      
      IF (current_shift_start_time_ <= sched_start_ AND current_shift_finish_time_ >= sched_start_) THEN
         shift_ := 'CURRENT_SHIFT';
      ELSIF (next_shift_start_time_ <= sched_start_ AND next_shift_finish_time_ >= sched_start_) THEN
         shift_ := 'NEXT_SHIFT';
      ELSIF (COALESCE(current_shift_start_time_, current_date_) > sched_start_ AND (execution_instance_status_ IS NULL OR execution_instance_status_ != 'Completed')) THEN
         shift_ := 'CURRENT_SHIFT';
      ELSE 
         FOR rec2_ IN Get_All_Shifts LOOP
            IF (next_shift_finish_time_ < sched_start_ AND rec2_.start_time <= sched_start_ AND rec2_.finish_time >= sched_start_) THEN
               shift_ := 'OTHER_SHIFTS';
               EXIT;
            END IF;
         END LOOP;
      END IF;
   END IF;
   RETURN shift_;
  END Get_Shift_By_Sched_Start; 

@IgnoreUnitTest TrivialFunction
FUNCTION Get_Assigned_Count_By_Shift (
   work_package_id_ IN NUMBER
) RETURN NUMBER
IS
   assign_to_me_count_ NUMBER := 0;
   current_user_ VARCHAR2(30) := Fnd_Session_API.Get_Fnd_User();
   
   CURSOR get_assign_to_me_count IS
   SELECT COUNT(*)
   FROM jt_task_resource_demand_av_uiv t
   WHERE t.assigned_resource_id = current_user_
   AND t.work_package_id = work_package_id_
   AND Flmexe_Util_API.Get_Shift_By_Sched_Start(t.sched_start, t.execution_instance_status) = 'CURRENT_SHIFT'
   AND t.task_status IN ('Active', 'In Work');
   
BEGIN
   IF work_package_id_ IS NOT NULL THEN
      OPEN get_assign_to_me_count;
      FETCH get_assign_to_me_count INTO assign_to_me_count_;
      CLOSE get_assign_to_me_count;
   END IF;
   
   RETURN assign_to_me_count_;
END Get_Assigned_Count_By_Shift;

@IgnoreUnitTest TrivialFunction
FUNCTION Get_Unassigned_Count_By_Shift (
   work_package_id_ IN NUMBER
) RETURN NUMBER
IS
   unassign_count_ NUMBER := 0;
   
   CURSOR get_unassign_to_me_count IS
   SELECT COUNT(*)
   FROM jt_task_resource_demand_av_uiv t
   WHERE t.assigned_resource_id IS NULL
   AND t.work_package_id = work_package_id_
   AND Flmexe_Util_API.Get_Shift_By_Sched_Start(t.sched_start, t.execution_instance_status) = 'CURRENT_SHIFT'
   AND t.task_status IN ('Active', 'In Work');
   
BEGIN
   IF work_package_id_ IS NOT NULL THEN
      OPEN get_unassign_to_me_count;
      FETCH get_unassign_to_me_count INTO unassign_count_;
      CLOSE get_unassign_to_me_count;
   END IF;
   
   RETURN unassign_count_;
END Get_Unassigned_Count_By_Shift;

@IgnoreUnitTest TrivialFunction
FUNCTION Get_A_Count_By_Next_Shift (
   work_package_id_ IN NUMBER
) RETURN NUMBER
IS
   assign_to_me_count_next_shift_ NUMBER := 0;
   current_user_ VARCHAR2(30) := Fnd_Session_API.Get_Fnd_User();
   
   CURSOR get_assign_to_me_count_next_shft IS
   SELECT COUNT(*)
   FROM jt_task_resource_demand_av_uiv t
   WHERE t.assigned_resource_id = current_user_ 
   AND t.work_package_id = work_package_id_
   AND Flmexe_Util_API.Get_Shift_By_Sched_Start(t.sched_start, t.execution_instance_status) = 'NEXT_SHIFT'
   AND t.task_status IN ('Active', 'In Work');
   
BEGIN
   IF work_package_id_ IS NOT NULL THEN
      OPEN get_assign_to_me_count_next_shft;
      FETCH get_assign_to_me_count_next_shft INTO assign_to_me_count_next_shift_;
      CLOSE get_assign_to_me_count_next_shft;
   END IF;
   
   RETURN assign_to_me_count_next_shift_;
END Get_A_Count_By_Next_Shift;

@IgnoreUnitTest TrivialFunction
FUNCTION Get_Work_Type_Text (
   is_heavy_maintenance_ IN NUMBER) RETURN VARCHAR2
IS
   work_type_ VARCHAR2(10) :=NULL;
BEGIN
	IF is_heavy_maintenance_ = 1 THEN
      work_type_:= 'Heavy';
   END IF;
   RETURN work_type_;
END Get_Work_Type_Text;

--Function To get Maintenance Location Time Zone for Faults
@IgnoreUnitTest TrivialFunction
FUNCTION Get_Fault_Maint_Location_T_Z (
   fault_id_ IN NUMBER) RETURN VARCHAR2
IS
   fault_state_         Av_Fault_Tab.rowstate%TYPE;
   location_timezone_   Av_Airport_Tab.airport_time_zone%TYPE;
   task_seq_            Av_Exe_Task.task_seq%TYPE;
   wp_id_               Av_Aircraft_Work_Package_Tab.aircraft_work_package_id%TYPE;
BEGIN
   fault_state_   := Av_Fault_API.Get_Objstate(fault_id_);
   task_seq_      := Av_Exe_Task_API.Get_Task_Seq(fault_id_);
   
   IF fault_state_ = 'Deferred' THEN
      wp_id_ := Av_Exe_Task_API.Get_Prev_Aircraft_Wp_Id(task_seq_);
   ELSE
      wp_id_ := Av_Exe_Task_API.Get_Aircraft_Wp_Id(task_seq_);
   END IF;
   location_timezone_ := Av_Maintenance_Location_API.Get_Location_Time_Zone(Av_Aircraft_Work_Package_API.Get_Location_Code(wp_id_));
   RETURN location_timezone_;
END Get_Fault_Maint_Location_T_Z;

@IgnoreUnitTest TrivialFunction
FUNCTION Handle_Null_In_Crew_Code (
   task_seq_ IN NUMBER) RETURN VARCHAR2
IS
   crew_code_  VARCHAR2(100);
BEGIN
    crew_code_ := Av_Exe_Task_API.Get_Crew_Code(task_seq_);
   IF crew_code_ IS NULL THEN
      RETURN '0';
   ELSE
      RETURN crew_code_;   
   END IF; 
END Handle_Null_In_Crew_Code;

@UncheckedAccess
@IgnoreUnitTest TrivialFunction
FUNCTION Is_Hangar_Supervisor RETURN VARCHAR2
IS
   role_              VARCHAR2(100):= 'HANGAR_SUPERVISOR';
BEGIN
   IF (Fnd_User_Role_API.Exists(Fnd_Session_API.Get_Fnd_User(), role_)) THEN
      RETURN 'TRUE';
   ELSE
      RETURN 'FALSE';
   END IF;
END Is_Hangar_Supervisor;

@UncheckedAccess
@IgnoreUnitTest TrivialFunction
FUNCTION Is_Hangar_Crew_Lead RETURN VARCHAR2
IS
   role_              VARCHAR2(100):= 'HANGAR_CREW_LEAD';
BEGIN
   IF (Fnd_User_Role_API.Exists(Fnd_Session_API.Get_Fnd_User(), role_)) THEN
      RETURN 'TRUE';
   ELSE
      RETURN 'FALSE';
   END IF;
END Is_Hangar_Crew_Lead;

-------------------- LU  NEW METHODS -------------------------------------
