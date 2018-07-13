////JavaScript file for interfacing with the Robot
//SDK = require
//SDK = require(['~/lib/microsoft-speech-browser-sdk/distrib/Speech.Browser.Sdk.js']);
//var robotURL = 'ws://localhost:9090';
var robotURL = 'ws://192.168.0.108:9090';

var numOfTodoItems = parseInt($('h5#itemsNum').text());
var numOfNotDoneItems = parseInt($('h5#notItemsNum').text());

var mealTypeName = $('h5#mealName').text();//'Rice and Stew';
var mealTypeDescription = $('h5#mealDes').text();//'The Meal is in the Fridge';

var drugTypeName = $('h5#drugName').text();//'Panadol';
var drugTypeDescription = $('h5#drugDes').text();//'Take two twice today';

var exerciseTypeName = $('h5#exerName').text();//'Mental and Physical Exercises';
var exerciseTypeDescription = $('h5#exerDes').text(); //'Check out the NHS guide on simple physical exercises and also do some brain games on your dashboard';

var miscTypeName = $('h5#miscName').text();//'Call Me';
var miscTypeDescription = $('h5#miscDes').text();//'Do not forget to video call me through your dashboard';


//ROS Publisher Variables
var todoListener;
var meal = mealTypeName + " with a description of: " + mealTypeDescription + ". ";
var drug = drugTypeName + " with a description of: " + drugTypeDescription + ". ";
var exercise = exerciseTypeName + " with a description of: " + exerciseTypeDescription + ". ";
var misc = miscTypeName + " with a description of: " + miscTypeDescription + ". ";

//Initialization of ROS Instance and Connection

var ros = new ROSLIB.Ros();
ros.connect(robotURL); //'ws:localhost:9090'


ros.on('connection', function () {
    console.log('Connected to web socket server.');
});
ros.on('error', function (error) {
    console.log('Error connecting to web socket server: ', error);
});
ros.on('close', function () {
    console.log('Connection to web socket server closed.');
});

//ROS Publishers


//Number of items in TodoList
numItems = new ROSLIB.Message({
    data: [numOfTodoItems,numOfNotDoneItems]
});

mealData = new ROSLIB.Message({
    data: meal
});

drugData = new ROSLIB.Message({
    data: drug
});

exerciseData = new ROSLIB.Message({
    data: exercise
});

miscData = new ROSLIB.Message({
    data: misc
});

var builder = [meal, drug, exercise, misc];
var intro;
if (numOfTodoItems !== 0) {
    intro = "You have " +
        numItems.data[0].toString() +
        " items on your To do list. With " +
        numItems.data[1].toString() +
        " items not done. Here is a summary: ";
    for (var tType in builder) {
        if (builder.hasOwnProperty(tType)) {
            if (builder[tType] !== " with a description of: . ") {
                intro += builder[tType];
            }

        }
    }
}
introData = new ROSLIB.Message({
    data:  intro

});


itemsListener = new ROSLIB.Topic({
    ros: ros,
    name: '/ItemsPublisher',
    messageType: 'std_msgs/Int32MultiArray'
});
if (numOfTodoItems !== 0)
{
    itemsListener.publish(numItems);
}



mealListener = new ROSLIB.Topic({
    ros: ros,
    name: '/MealPublisher',
    messageType: 'std_msgs/String'
});
if (mealData.data !== " with a description of: . ") {
    mealListener.publish(mealData);
}



drugListener = new ROSLIB.Topic({
    ros: ros,
    name: '/DrugPublisher',
    messageType: 'std_msgs/String'
});
if (drugData.data !== " with a description of: . ") {
    drugListener.publish(drugData);
}



exerciseListener = new ROSLIB.Topic({
    ros: ros,
    name: '/ExercisePublisher',
    messageType: 'std_msgs/String'
});
if (exerciseData.data !== " with a description of: . ") {
    exerciseListener.publish(exerciseData);
}



miscListener = new ROSLIB.Topic({
    ros: ros,
    name: '/MiscPublisher',
    messageType: 'std_msgs/String'
});
if (miscData.data !== " with a description of: . ") {
    miscListener.publish(miscData);
}

introListener = new ROSLIB.Topic({
    ros: ros,
    name: '/IntroPublisher',
    messageType: 'std_msgs/String'
});
if (numOfTodoItems !== 0) {
    introListener.publish(introData);
}

langListener = new ROSLIB.Topic({
    ros: ros,
    name: '/LangPublisher',
    messageType: 'std_msgs/String'
});
langdata = $('input[name=lang]:checked').val();
function langPublish() {
    console.log("Writing Language DATA");
    console.log(langdata);
    var langData = new ROSLIB.Message({
        data: langdata
    });
    langListener.publish(langData);
};
langPublish()
sttListener = new ROSLIB.Topic({
    ros: ros,
    name: '/StartSTTPublisher',
    messageType: 'std_msgs/Bool'
});

startSTTData = false;

function startSTTPublish() {
    console.log("Sending Start STT DATA");
    console.log(startSTTData);
    var sttData = new ROSLIB.Message({
        data: startSTTData
    });
    sttListener.publish(sttData);
};

queryPublisher = new ROSLIB.Topic({
    ros: ros,
    name: "/QueryResultPublisher",
    messageType: "std_msgs/String"
});


//ROS Subscribers
querySubscriber = new ROSLIB.Topic({
    ros: ros,
    name: "/todoListQueryPublisher",
    messageType: "std_msgs/Int32MultiArray"
});

querySubscriber.subscribe(function(message) {
    console.log("Recieved data " + message.data);
    if (message.data[0] === 1) {
        //Set
        $.ajax(
            {
                url: '/Home/ShevaUpdateKaban',
                type: "POST",
                dataType: "json",
                data: {
                    crud: message.data[0],
                    item: message.data[1],
                    number: message.data[2],
                    ordinal: message.data[3]
                },
                success: function () {
                    console.log("Sheva has updated your list");
                }
            });
        
    } else {
        //get
        $.ajax(
            {
                url: '/Home/QueryKaban',
                type: "GET",
                dataType: "json",
                data: {
                    crud: message.data[0],
                    item: message.data[1],
                    number: message.data[2],
                    ordinal: message.data[3],
                    status: message.data[4]
                },
                success: function(response) {
                    var result = new ROSLIB.Message(
                        {
                            data: response
                        });
                    queryPublisher.publish(result);
                    console.log("Query done " + response);

                }
            });
    }
    
});