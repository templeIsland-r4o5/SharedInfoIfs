/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 * ---------------------------------------------------------------------------
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmFaultDeferral
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
import javax.ejb.Stateless;
import java.sql.Connection;
import java.util.HashMap;
import java.util.Map;


/*
 * Implementation class that contains Read, Update and Delete methods for Stream type entity attributes
 * which are marked with implementation = "Java" in the FlmFaultDeferral projection model.
 */
@Stateless(name = "FlmFaultDeferralStreamAttributesHandler")
public class FlmFaultDeferralStreamAttributesHandlerImpl implements FlmFaultDeferralStreamAttributesHandler {

   @Override
   public Map<String, Object> readFaultDefMainVirtualMediaObject(final Map<String, Object> parameters, final Connection connection) {
      Map<String, Object> returnMap = new HashMap<>();
      try {
         MediaItemUtil mediaUtil = new MediaItemUtil();
         EsignLogoUtil logoUtil = new EsignLogoUtil();
         String objkey = (String) parameters.get("Objkey");
         if (objkey != null) {
            Map<String, Object> itemIdMap = logoUtil.getMediaItemId(objkey, "FaultDeferral", connection);
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
   public Map<String, Object> updateFaultDefMainVirtualMediaObject(final Map<String, Object> parameters, final Connection connection) {
      throw new UnsupportedOperationException("Not supported yet.");
   }

   @Override
   public Map<String, Object> deleteFaultDefMainVirtualMediaObject(final Map<String, Object> parameters, final Connection connection) {
      throw new UnsupportedOperationException("Not supported yet.");
   }
}
