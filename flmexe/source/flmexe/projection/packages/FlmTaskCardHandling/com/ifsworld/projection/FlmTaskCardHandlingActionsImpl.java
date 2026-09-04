/*
 *  Template:     3.0
 *  Built by:     IFS Developer Studio
 *
 *
 *
 * ---------------------------------------------------------------------------
 *
 *  Logical unit: FlmTaskCardHandling
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
 * Implementation class for all global actions defined in the FlmTaskCardHandling projection model.
 */

@Stateless(name="FlmTaskCardHandlingActions")
@TransactionAttribute(value = TransactionAttributeType.REQUIRED)
public class FlmTaskCardHandlingActionsImpl extends FlmTaskCardHandlingActionsFragmentsWrapper implements FlmTaskCardHandlingActions {
}