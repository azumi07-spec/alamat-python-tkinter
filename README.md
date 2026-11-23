ALAMAT - Philippine Folklore Quiz
Name: AzumiPearl A. Benig 
Course: BS InfoTech
Section: SE 3-A

Topic: 
Creatures of Philippine folklore, specifically those that are still being talked about up to this day in provinces (kapre, dwende, diwata, aswang, tikbalang and more)

Description:
A Tkinter desktop quiz with a black, maroon, and red color theme, and bold fonts. It has 10 multiple-choice questions, a 15-second timer per question, an answer review, and a saved high score. Each question was written out of basic knowledge gathered from the elders and based on some research on the internet.

Design:
A color scheme of red and maroon, with black serving as a complementary hue. The layout and fonts are adjusted to fit the window size when the game opens in full screen mode (F11 toggles full screen, Esc leaves it). When installed, Impact is used for headings and Bahnschrift is used for body text (other bold fonts are used as a backup). In order to distinguish them from the red incorrect answers, correct answers are indicated in green.

Features:
Ten questions, each with four options; the order is shuffled. 15-second countdown with a progress bar, time-out management, automatic answer verification, no duplicate submissions, and score monitoring. "Question X of 10" indicator, results screen with message and percentage, answer review, high score stored in high_score.txt, restart button, optional player name, and color feedback.



Questions: 
  Kept in a list named QUESTIONS. Every question is a dictionary that includes a question, four strings beginning with the letters A through D as options, and an answer (the right letter). Every time start_quiz() executes, random.sample() creates a shuffled copy, ensuring that the initial list remains unchanged.

Timer: 
  Update_timer() displays time_left, deducts 1, and reschedules itself using root.after(1000,...). Timer_job is where the job ID is stored. As soon as an answer is submitted, stop_timer() calls root.after_cancel() on it. Time_up() executes at 0 seconds.
  
Correct answer: 
  Selected_answer.get() returns "A"–"D" since the value of each radio button is its letter. It is compared with question ("answer") by submit_answer().

Score: 
  For every right response, the score increases by one. (Score/Total) * 100 is the percentage.

High score:
  The number from high_score.txt is read by get_high_score() (0 if the file is invalid or missing). Only when the new score is higher does save_high_score() overwrite the file.It is called on the results screen.
  
Functions:

Function	            Purpose	Called when
start_quiz()	        Resets variables and shuffles the questions	Launch or Restart is clicked
show_question()	      Builds the question screen and starts the timer	Each new question
update_timer()	      Shows time left and counts down every second	A question is displayed
stop_timer()	        Cancels the scheduled timer call	Submit, time-up, closing
submit_answer()	      Checks the answer and updates the score	Submit is clicked
time_up()	            Marks the question wrong when time runs out	Timer reaches 0
save_high_score()	    Writes the score if it is higher	Results screen is shown
show_results()	      Shows score, percentage, message, review	After question 10



CONCLUSION:
  Players test their knowledge of Philippine folklore creatures like the kapre, aswang, diwata, and tikbalang in the desktop quiz game ALAMAT, which was created using Python's Tkinter. The player can choose to type their name before clicking the start button on the start screen, which displays the number of questions, the time limit, and the saved high score.

  Each of the quiz's ten multiple-choice questions has four options (A through D) and only one right answer. The questions' order is changed each time the game launches or restarts. The screen displays the current question number (e.g., "Question 4 of 10"), the score, and the remaining time for each question. The player has 15 seconds to select an answer and click Submit. The response is automatically verified; a right response earns one point and is indicated, while an incorrect response is marked and the correct response is made clear.

  A question cannot be answered twice because the timer stops and the choices are locked after an answer is submitted. If the player clicks Submit without making a selection, a warning will appear and the timer will continue to run. The question is deemed incorrect and the right response is displayed if the player runs out of time before submitting. Following the final question, the results screen shows the final score, the percentage, and a performance message based on the player's performance. It also includes a review that lists all of the questions that were answered incorrectly along with the player's response and the correct response.

  The player is informed when they have set a new record, and the highest score is stored in a text file, so it remains there even after the program is closed and reopened. Lastly, the player has the option to exit the game, go back to the start screen, or restart the quiz for a new, rearranged round.

  SCREEN SHOTS:
  Start Screen:
  <img width="1366" height="768" alt="start" src="https://github.com/user-attachments/assets/b4961b36-7dec-431a-9bd4-b73a6c075f07" />

  Question with Timer:
  <img width="1366" height="768" alt="question" src="https://github.com/user-attachments/assets/44a0d7be-ba99-4b16-a2fe-6bef8e96c319" />

  Answer Feedback:
  <img width="1366" height="768" alt="feedback" src="https://github.com/user-attachments/assets/03c57bef-3172-4727-8545-ad591f3a4b68" />

  Result and Answer Review:
  <img width="1366" height="768" alt="result" src="https://github.com/user-attachments/assets/c326435c-f927-431a-a371-270484ff0fd9" />

  High Score:
  <img width="1366" height="768" alt="high_score" src="https://github.com/user-attachments/assets/cb19df48-0d8e-4740-8bdf-6a32afc2901b" />



