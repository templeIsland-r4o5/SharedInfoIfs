/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmMyWorksHandling
 *  Component:    FLMEXE
 *
 * ---------------------------------------------------------------------------
 */

package com.ifsworld.projection;

import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import java.io.InputStream;
import java.sql.Connection;
import java.util.Map;

/*
 * Implementation class for all global actions defined in the FlmMyWorksHandling projection model.
 */

@Stateless(name="FlmMyWorksHandlingActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmMyWorksHandlingActionsImpl extends FlmMyWorksHandlingActionsFragmentsWrapper implements FlmMyWorksHandlingActions {
}