from .metrics import Metric
from .descriptions import Description
from .relevant import get_relevant_answers

# Instantiate metrics
# Note: description_beginner, description_intermediate, description_master, definition should use html format for tooltip fomatting purpose
metrics = {
    "planner": Metric(
        "Planner",
        "img/planner.png",
        "You can plan lessons and assessments with some level of professionalism and organization. You prepare basic lesson plans and use a limited range of assessment methods. While you consider students' abilities to some extent, you may not always tailor resources and time allocation effectively. You follow instructions but may need reminders or support to ensure compliance.",
        "You plan lessons and assessments in a professional and systematic manner. You develop detailed and comprehensive lesson plans that incorporate a variety of assessment methods. You use students' abilities to differentiate instruction and provide appropriate educational resources. You allocate time effectively and comply with instructions without much need for supervision. Overall, You are skilled planners who can contribute to effective teaching and learning.",
        "You fully meet the definition! Congrats!",
        "Plan the implementation of PdPc professionally and systematically.<br>Prepare lesson plans and determine appropriate assessment methods.<br>Provide educational resources according to students' abilities, time allocation, and adherence to the instructions in force."
    ),
    "guardian": Metric(
        "Guardian",
        "img/guardian.png",
        "You are able to control the learning process to some extent, but you may not always do so in a fully professional and organized manner. You manage the content of the lesson and allocate time, but you may not always provide opportunities for active student participation or fully meet learning objectives. You may need to improve your skills as a guardian to ensure effective teaching and learning, such as monitoring student communication and behavior more closely or creating a more engaging learning environment.",
        "You are able to control the learning process in a professional and organized manner. You manage the content of the lesson and allocate time effectively, and provide opportunities for active student participation to meet learning objectives. You control the learning environment well, by monitoring student communication and behavior and arranging the position of students to create an engaging learning environment. You are a skilled guardian who can contribute to effective teaching and learning.",
        "You fully meet the definition! Congrats!",
        "Control the learning process and learning environment in a professional and organized manner.<br>Manages the content of the lesson and the allocation of time given.<br>Provide opportunities for active participation of students by meeting the learning objectives and according to the ability of students to learn.<br>Monitor student communication and behavior.<br>Arrange the position of students and create an entertaining learning environment."
    ),
    "mentor": Metric(
        "Mentor",
        "img/mentor.png",
        "You can guide students to some extent, but may not always do so effectively as a mentor. You assist in mastering the content and skills based on the syllabus, but may not always guide students to make decisions and solve problems in learning activities. You may need to improve your skills as a mentor, such as by providing more opportunities for student decision-making and problem-solving, and offering more personalized guidance.",
        "You are a skilled mentor who guides students effectively in their learning activities. You assist in mastering the content and skills based on the syllabus, and guide students to make decisions and solve problems in learning activities. You offer personalized guidance that is tailored to individual student needs, and provide opportunities for student reflection and feedback. Your mentorship contributes to students' growth and development, and fosters a positive learning environment.",
        "You fully meet the definition! Congrats!",
        "Guide students to master the content and skills based on the syllabus.<br>Assist students make decisions and solve problems in learning activities."
    ),
    "motivator": Metric(
        "Motivator",
        "img/motivator.png",
        "You encourage students' minds and emotions to some extent, but may not always do so in a fully professional and planned manner as a motivator. You stimulate students to communicate and collaborate by asking questions, but may not always focus on critical and creative thinking. You may not always encourage students to make decisions or solve problems during learning activities. You may also not always provide adequate emotional support to students, such as by giving praise, encouragement, appreciation, confidence, and concern for their needs. You need to improve your skills as a motivator to create a more positive learning environment.",
        "You are a skilled motivator who encourages students' minds and emotions effectively in their learning activities. You stimulate students to communicate and collaborate by asking questions that promote critical and creative thinking. You encourage students to make decisions or solve problems during learning activities, and provide them with appropriate support and feedback. You also give praise, encouragement, appreciation, confidence, and concern for the needs of students in a professional, planned, and comprehensive manner. Your motivation inspires and empowers students to reach their full potential in learning.",
        "You fully meet the definition! Congrats!",
        "Encourage students' minds and emotions in carrying out learning activities in a professional and planned manner.<br>Mind motivators stimulate students to communicate and collaborate by asking questions geared toward critical and creative thinking.<br>Encourage students to make decisions or solve problems when learning activities are carried out.<br>Emotional motivators give praise, encouragement, appreciation, and confidence as well as<br>concern for the needs of students in a prudent, comprehensive, and continuous manner."
    ),
    "assessor": Metric(
        "Assessor",
        "img/assessor.png",
        "You perform assessments to some extent, but may not always do so in a fully systematic and planned manner as an assessor. You use some assessment methods, but may not use them effectively or appropriately. You may not conduct intervention activities, give assignments, or review student work as consistently or thoroughly as needed. You may need to improve your skills as an assessor to ensure that your assessments are accurate and meaningful, and that your feedback supports students' learning.",
        "You are a skilled assessor who performs assessments in a systematic and planned manner. You use a variety of assessment methods effectively, and conduct intervention activities, give assignments, and review student work to monitor progress and provide feedback. You reflect on assessment results and adjust teaching strategies accordingly. Your assessments are accurate and meaningful, and your feedback supports students' learning and growth. Your assessments also comply with the relevant policies and standards, and contribute to the overall quality of education.",
        "You fully meet the definition! Congrats!",
        "Perform assessments in a systematic and planned manner. evaluators, teachers<br>Use various assessment methods, conduct intervention activities, give assignments, reflect on and review student work."
    ),
}
