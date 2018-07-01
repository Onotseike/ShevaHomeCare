//JavaScript file for interfacing with the Robot


var robotURL = 'ws://localhost:9090';

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
    data: mealTypeName + " with a description of: " + mealTypeDescription
});

drugData = new ROSLIB.Message({
    data: drugTypeName + " with a description of: " + drugTypeDescription
});

exerciseData = new ROSLIB.Message({
    data: exerciseTypeName + " with a description of: " + exerciseTypeDescription
});

miscData = new ROSLIB.Message({
    data: miscTypeName + " with a description of: " + miscTypeDescription
});


itemsListener = new ROSLIB.Topic({
    ros: ros,
    name: '/ItemsPublisher',
    messageType: 'std_msgs/Int32MultiArray'
});
itemsListener.publish(numItems);


mealListener = new ROSLIB.Topic({
    ros: ros,
    name: '/MealPublisher',
    messageType: 'std_msgs/String'
});
mealListener.publish(mealData);


drugListener = new ROSLIB.Topic({
    ros: ros,
    name: '/DrugPublisher',
    messageType: 'std_msgs/String'
});
drugListener.publish(drugData);


exerciseListener = new ROSLIB.Topic({
    ros: ros,
    name: '/ExercisePublisher',
    messageType: 'std_msgs/String'
});
exerciseListener.publish(exerciseData);


miscListener = new ROSLIB.Topic({
    ros: ros,
    name: '/MiscPublisher',
    messageType: 'std_msgs/String'
});
miscListener.publish(miscData);

langListener = new ROSLIB.Topic({
    ros: ros,
    name: '/LangPublisher',
    messageType: 'std_msgs/String'
});
langdata = ""
function langPublish() {
    console.log("Writing Language DATA");
    console.log(langdata);
    langListener.publish(langdata);
}