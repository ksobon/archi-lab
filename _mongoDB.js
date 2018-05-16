// Add new field to all objects in a given collection
db.configurations.update(
  {}, 
  {$set: {
    "sharedParamMonitor": {
      _id: ObjectId(), 
      "monitorId": "32d44b45-7bf6-49f1-9b81-f41ae929cfcb", 
      "monitorName": "Shared Parameter Monitor", 
      "description": "This tool will monitor and make sure that the appropriate Shared Parameter file is being used on the project.", 
      "filePath": " ", 
      "addInName": "Mission Control", 
      "isMonitorOn": false}}}, 
  true, 
  true)

// update specific field value by matching the updater id
db.configurations.update(
  {"updaters.updaterId": "90391154-67BB-452E-A1A7-A07A98B94F86"},
  {$set: {"updaters.description": "This tool will prevent users from Unloading Linked Revit files for \"all users\" which causes such Linked File to be unloaded by default when opening project."}},
  {multi: true}
)
// add/update field for every object in an array
db.addins.find({
   "usageLogs":{"$exists":true}}).forEach(function(data){
    for(var i=0;i<data.usageLogs.length;i++) {
      db.addins.update(
        {"_id": data._id, "usageLogs._id": data.usageLogs[i]._id},
        {"$set": {"usageLogs.$.test": false}},
        true,
        true
        );
    }
})
// removes a field from a nested object
db.addins.find({
   "usageLogs":{"$exists":true}}).forEach(function(data){
    for(var i=0;i<data.usageLogs.length;i++) {
      db.addins.update(
        {"_id": data._id, "usageLogs._id": data.usageLogs[i]._id},
        {"$unset": {"usageLogs.$.executionTime": ""}},
        true,
        true
        );
    }
})
//remove field from object
db.getCollection('healthrecords').update(
    {},
    {$unset: {familyStats: ""}},
    {multi: true}
)
//add/update field on oject
db.getCollection('healthrecords').update(
    {},
    {$set: {familyStats: null}},
    true,
    true
)
//set sheets to empty array
db.getCollection('projects').update(
    {},
    {$set: {sheets: []}},
    true,
    true
)
// set user name to lower case
db.addins.find({
   "usageLogs":{"$exists":true}}).forEach(function(data){
    for(var i=0;i<data.usageLogs.length;i++) {
      db.addins.update(
        {"_id": data._id, "usageLogs._id": data.usageLogs[i]._id},
        {"$set": {"usageLogs.$.user": data.usageLogs[i].user.toLowerCase()}},
        true,
        true
        );
    }
})
//insert an empty array into an array in revers
//needed this when it errored out doing it forwards
db.addins.find({
   "usageLogs":{"$exists":true}}).forEach(function(data){
    for(var i = data.usageLogs.length; i--;) {
      db.addins.update(
        {"_id": data._id, "usageLogs._id": data.usageLogs[i]._id},
        {"$set": {"usageLogs.$.detailInfo": []}},
        {"upsert": true}
        );
    }
})
//update all nested objects with a matching value
var query = {
    usageLogs: {
        $elemMatch: {
            user: "konrad.sobon",
            office: { $ne: "NY" }
        }
    }
};

while (db.addins.find(query).count() > 0) {
    db.addins.update(
        query,
        { $set: { "usageLogs.$.office": "NY" } },
        { multi: true }
    );
}
//update all central path values to lower case.
db.triggerrecords.find().forEach(
  function(e) {
    e.centralPath = e.centralPath.toLowerCase();
    db.triggerrecords.save(e);
  }
)
//add new user overrides object to all health record updaters
db.configurations.find().forEach(function(e) {
    e.updaters.forEach(function(updater){
        if (updater.updaterId == "56603be6-aeb2-45d0-9ebc-2830fad6368b"){
            updater["userOverrides"] = {
                "familyNameCheck": {
                    "description": "Family Name Check:",
                    "values": ["HOK_I", "HOK_M"]
                    },
                "dimensionValueCheck": {
                    "description": "Dimension Override Check:",
                    "values": ["EQ"]
                    }
                }
            }
        })
    db.configurations.save(e);
  }
)

db.triggerrecords.find({'centralPath': { $regex : new RegExp("rsn://ny-28svr/13.07051.00 laguardia terminal b/ar/a12801375-3d-hhenc_central.rvt", "i") } }).forEach(function(doc){
	db.triggerrecords2.update({'_id': ObjectId("5af0977625f7db49c4dfd2d8")}, {$push: {triggerRecords: doc}})
});

// find a configuratio by central path
db.configurations.find().forEach(function(e) {
    e.files.forEach(function(file){
      	var result = file.centralPath.match(/nashyards/i);
      	if (result){
      		print(e._id);
      	}
  	})
})
