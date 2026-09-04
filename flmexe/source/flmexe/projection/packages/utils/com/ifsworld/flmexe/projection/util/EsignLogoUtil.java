/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 *
 * ---------------------------------------------------------------------------
 * Date    Sign     Comment
 * ----------------------------------------------------------------------------
 * 240430  KAWJLK  AD-10914, Created.
 * ---------------------------------------------------------------------------
 */
package com.ifsworld.flmexe.projection.util;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;
import java.sql.CallableStatement;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author kawjlk
 */
public class EsignLogoUtil {

   static final Logger LOGGER = Logger.getLogger(EsignLogoUtil.class.getName());

   public Map<String, Object> getMediaItemId(String objkey, String source, Connection connection) throws SQLException {

      Map<String, Object> returnMap = new HashMap<>();

      if (objkey != null) {
         CallableStatement stmt = null;
         try {
            stmt = connection.prepareCall("{call Av_Esign_Logo_API.Retrieve_Logo_Item_By_Source(?, ?, ?)}");
            stmt.setString(1, objkey);
            stmt.setString(2, source);
            stmt.registerOutParameter(3, java.sql.Types.INTEGER);
            stmt.execute();

            int itemId = stmt.getInt(3);
            returnMap.put("ItemId", itemId);

         } catch (SQLException e) {
            throw new SQLException("Failed to fetch ItemId: " + e.getMessage());
         } finally {
            if (stmt != null) {
               stmt.close();
            }
         }
      } else {
         LOGGER.log(Level.WARNING, "objkey parameter not found or null/empty.");
      }
      return returnMap;
   }
}
