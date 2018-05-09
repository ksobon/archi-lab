var projectId = 
ObjectId("5aecd4e0a7f2973820443595")
;
var healthRecordId = 
ObjectId("5aecd81fa7f29738204438b9")
;
var centralPath = 
"\\\\group\\hok\\sf\\projects\\2014\\14.72018.00 summerlin, nv aaa ballpark 149300.00\\e-design\\e6-models\\revit\\aaa-hok-ar-central.rvt"
;

//
//
// STYLES
//
//


var stylesId = ObjectId();

//create new collection in styles and populate it with document from health records
var styleStats = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'styleStats': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!styleStats.styleStats){
	styleStats = [];
} else {
	styleStats = styleStats.styleStats;
}
	
db.styles.insert(
{
  "_id": stylesId,
  "centralPath": centralPath,
  "styleStats" : styleStats
  }
);

//update project collection with new document reference
db.projects.update({_id: projectId}, {$push: {"styleStats": stylesId }});


//
//
// WORKSETS
//
//


var worksetsId = ObjectId();

//create new collection in styles and populate it with document from health records
var onOpened = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'onOpened': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});
	
if (!onOpened.onOpened){
	onOpened = [];
} else {
	onOpened = onOpened.onOpened;
}
	
var onSynched = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'onSynched': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!onSynched.onSynched){
	onSynched = [];
} else {
	onSynched = onSynched.onSynched;
}
	
var itemCount = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'itemCount': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!itemCount.itemCount){
	itemCount = [];
} else {
	itemCount = itemCount.itemCount;
}
	
db.worksets.insert(
{
  "_id": worksetsId,
  "centralPath": centralPath,
  "onOpened" : onOpened,
  "onSynched" : onSynched,
  "itemCount" : itemCount
  }
);

//update project collection with new document reference
db.projects.update({_id: projectId}, {$push: {"worksetStats": worksetsId }});



//
//
// VIEWS
//
//



var viewsId = ObjectId();

//create new collection in styles and populate it with document from health records
var viewStats = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'viewStats': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!viewStats.viewStats){
	viewStats = [];
} else {
	viewStats = viewStats.viewStats;
}
	
db.views.insert(
{
  "_id": viewsId,
  "centralPath": centralPath,
  "viewStats" : viewStats
  }
);

//update project collection with new document reference
db.projects.update({_id: projectId}, {$push: {"viewStats": viewsId }});



//
//
// LINKS
//
//



var linksId = ObjectId();

//create new collection in styles and populate it with document from health records
var linkStats = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'linkStats': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!linkStats.linkStats){
	linkStats = [];
} else {
	linkStats = linkStats.linkStats;
}
	
db.links.insert(
{
  "_id": linksId,
  "centralPath": centralPath,
  "linkStats" : linkStats
  }
);

//update project collection with new document reference
db.projects.update({_id: projectId}, {$push: {"linkStats": linksId }});



//
//
// MODELS
//
//



var modelsId = ObjectId();

//create new collection in styles and populate it with document from health records
var modelSizes = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'modelSizes': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!modelSizes.modelSizes){
	modelSizes = [];
} else {
	modelSizes = modelSizes.modelSizes;
}
	
var synchTimes = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'synchTimes': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!synchTimes.synchTimes){
	synchTimes = [];
} else {
	synchTimes = synchTimes.synchTimes;
}
	
var openTimes = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'openTimes': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!openTimes.openTimes){
	openTimes = [];
} else {
	openTimes = openTimes.openTimes;
}
	
db.models.insert(
{
  "_id": modelsId,
  "centralPath": centralPath,
  "modelSizes" : modelSizes,
  "synchTimes" : synchTimes,
  "openTimes" : openTimes
  }
);

//update project collection with new document reference
db.projects.update({_id: projectId}, {$push: {"modelStats": modelsId }});



//
//
// FAMILIES
//
//




//create new collection in styles and populate it with document from health records
var familiesId = db.healthrecords.find(
	{_id: healthRecordId}, 
	{_id: 0, 'familyStats': 1}).toArray().reduce(function(acc, val){acc.concat(val), []});

if (!familiesId.familyStats || familiesId.familyStats == null){
	//do nothing
} else {
	//update project collection with new document reference
	db.projects.update({_id: projectId}, {$push: {"familyStats": familiesId.familyStats }});
}


//
//
// TRIGGER RECORDS
//
//


var recordsId = ObjectId();

db.triggerrecords2.insert(
{
  "_id": recordsId,
  "centralPath": centralPath,
  "triggerRecords" : []
  }
);

db.triggerrecords.find({'centralPath': { $regex : new RegExp(centralPath, "i") } }).forEach(function(doc){
	db.triggerrecords2.update({'_id': recordsId}, {$push: {'triggerRecords': doc}})
});

//update project collection with new document reference
db.projects.update({_id: projectId}, {$push: {"triggerRecords": recordsId }});
