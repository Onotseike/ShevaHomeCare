//JavaScript file for interfacing with the Robot


var robotURL = "";

var numOfTodoItems = 4;
var numOfNotDoneItems = 3;

var mealTypeName = 'Rice and Stew';
var mealTypeDescription = 'The Meal is in the Fridge';

var drugTypeName = 'Panadol';
var drugTypeDescription = 'Take two twice today';

var exerciseTypeName = 'Mental and Physical Exercises';
var exerciseTypeDescription =
    'Check out the NHS guide on simple physical exercises and also do some brain games on your dashboard';

var miscTypeName = 'Call Me';
var miscTypeDescription = 'Do not forget to video call me through your dashboard';


//ROS Publisher Variables
var todoListener;


//Initialization of ROS Instance and Connection

var ros = new ROSLIB.Ros();
ros.connect(robotURL); //'ws:localhost:9090'

//ROS Publishers
todoListener = new ROSLIB.Topic({
    ros: ros,
    name: '/ToDoItemsPublisher',
    messageType: 'sheva_ros_pk/kabanitems'
});

kabanMsg = new ROSLIB.Message(
    {
        num_of_items: numOfTodoItems,
        num_not_items: numOfNotDoneItems,

        meal_name: mealTypeName,
        meal_description: mealTypeDescription,

        drug_name: drugTypeName,
        drug_description: drugTypeDescription,

        exercise_name: exerciseTypeName,
        exercise_description: exerciseTypeDescription,

        misc_name: miscTypeName,
        misc_description: miscTypeDescription
    });

todoListener.publish(kabanMsg);






