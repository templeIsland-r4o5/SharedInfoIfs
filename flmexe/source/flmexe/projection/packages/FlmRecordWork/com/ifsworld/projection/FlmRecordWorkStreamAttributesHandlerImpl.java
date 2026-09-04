/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 * ---------------------------------------------------------------------------
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmRecordWork
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 * Date    Sign    Comment
 * ----------------------------------------------------------------------------
 * 240416  KAWJLK  AD-10914, Created.
 * ---------------------------------------------------------------------------
 */
package com.ifsworld.projection;

import com.ifsworld.appsrv.projection.util.MediaItemUtil;
import com.ifsworld.flmexe.projection.util.EsignLogoUtil;
import com.ifsworld.fnd.odp.api.exception.ProjectionException;
import java.sql.CallableStatement;
import javax.ejb.Stateless;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;


/*
 * Implementation class that contains Read, Update and Delete methods for Stream type entity attributes
 * which are marked with implementation = "Java" in the FlmRecordWork projection model.
 */
@Stateless(name = "FlmRecordWorkStreamAttributesHandler")
public class FlmRecordWorkStreamAttributesHandlerImpl implements FlmRecordWorkStreamAttributesHandler {

   @Override
   public Map<String, Object> readRecordWorkVirtualMediaObject(final Map<String, Object> parameters, final Connection connection) {
      Map<String, Object> returnMap = new HashMap<>();
      try {
         MediaItemUtil mediaUtil = new MediaItemUtil();
         EsignLogoUtil logoUtil = new EsignLogoUtil();
         String objkey = (String) parameters.get("Objkey");
         if (objkey != null) {
            Map<String, Object> itemIdMap = logoUtil.getMediaItemId(objkey, "RecordWork", connection);
            parameters.putAll(itemIdMap);
         }
         returnMap = mediaUtil.readMediaItem(parameters, connection);

      } catch (ProjectionException ex) {
         throw new ProjectionException(ex.getMessage(), ex, ex.getCustomCode());
      } catch (Exception ex) {
         throw new ProjectionException(ex.getMessage(), ex);
      }
      return returnMap;
   }

   @Override
   public Map<String, Object> updateRecordWorkVirtualMediaObject(final Map<String, Object> parameters, final Connection connection) {
      throw new UnsupportedOperationException("Not supported yet.");
   }

   @Override
   public Map<String, Object> deleteRecordWorkVirtualMediaObject(final Map<String, Object> parameters, final Connection connection) {
      throw new UnsupportedOperationException("Not supported yet.");
   }

}
