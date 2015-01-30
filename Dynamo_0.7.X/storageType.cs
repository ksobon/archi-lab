using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Xml;
using DSCoreNodesUI;
using Dynamo.Models;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Analysis;

namespace EnergyAnalysisForDynamo_UI
{
    [NodeName("Storage Type")]
    [NodeCategory("Grimshaw.Selection")]
    [NodeDescription("Select a Storage Type to use with Create Shared Parameter node")]
    [IsDesignScriptCompatible]
    public class BuildingTypeDropdown : EnumAsString<StorageType>
    {
        public BuildingTypeDropdown(WorkspaceModel workspace) : base(workspace) { }
    }

}
