/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmMyPartRequestHandling
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
 * Implementation class for all global actions defined in the FlmMyPartRequestHandling projection model.
 */

@Stateless(name="FlmMyPartRequestHandlingActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmMyPartRequestHandlingActionsImpl extends FlmMyPartRequestHandlingActionsFragmentsWrapper implements FlmMyPartRequestHandlingActions {
}