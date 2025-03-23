templates = {
	"Auswählen...": {
		"korrektur": "",
		"arbeitsanweisung": "",
		"template": ""
	},
	"Englisch Bildbeschreibung": {
		"korrektur": """
Scope: You are a high school teacher and have to grade class work.
Input: Input are one or more text documents, headed by <<TEXT_1>>...<<TEXT_N>>.
Output: Output is a single HTML document with headings TEXT_1..TEXT_N.

The document contains per TEXT a table A() with 2 columns. Both columns having the same width.
In the left column (AL) is the uncorrected original with all errors, the right column (AR) is the corrected version.

Correct and annotate in the right column (AR), but only colorize changed parts:
CRITERION_SPELLING_SPELLING: Upper and lower case, incorrect spelling. Annotate mistakes in red color.
CRITERION_SPELLING_PUNCTUATION: Period, comma and special characters, citation rules. Annotate mistakes in red color.
CRITERION_SPELLING_STRUCTURE: Grammar and incorrect or missing words. Annotate mistakes in red color.

Propose improvements in the right column (AR) in blue color:
CRITERION_CONTENT_STYLE: Readability and comprehensibility in the sentence and in the entire text.
CRITERION_CONTENT_CREATIVITY: Information content of the text.
CRITERION_CONTENT_SCOPE: Extent of the text.
CRITERION_CONTENT_QUESTIONS: Completeness of answers to the questions, if questions are asked by the teacher.

Per TEXT add a table (B) underneath with columns. Be polite in with the justification.
|Criterion|Possible Score|Achieved Score|Justification|
Sum up the points for CRITERION_SPELLING in the last row.
Sum up the points for CRITERION_CONTENT in the last row.


Calculate the score for the CRITERIONS in range 1..10 and consider all TEXT inputs to allow direct comparison.
Use the template here:
"""
,

"arbeitsanweisung":
"""
Language is british english. The children have been learning english for half a year. Consider this for the justification.


Task description:

You are on holiday with your family. You have a great house there. It's your dream house!

Write an email to your friend. Write about
- which rooms there are
- which things you can find there and what colour they are
- which room you like best
- what you do in your house

Write about ten sentences!

Here is the result to be evaluated:
""",

"template":
"""
<h1>TEXT_1</h1>
<table style="width:100%">
  <tr>
    <th>Original Text</th>
    <th>Corrected Text</th>
  </tr>
  <tr>
    <td>We have a cool house here</td>
    <td>We have a cool house <font color="red">here</font>. <font color="green">Consider starting with a more formal greeting in an email.</font></td>
  </tr>
  <tr>
    <td>at Upstairs there's the quit chamber, the control room the living room, the toranga and the guest room.</td>
    <td>Upstairs, <font color="red">there is</font> the quiet chamber, the control room, the living room, <font color="red">the lounge</font> (or <font color="red">living area</font>), and the guest room. <font color="green">You may want to explain what a "toranga" is, as it's not a standard term.</font></td>
  </tr>
  <tr>
    <td>At the second floor there's my and me brother's rooms, the kitchen, the dininig room, and a cool.</td>
    <td>On the second floor, <font color="red">there are</font> my and my brother's rooms, the kitchen, the <font color="red">dining</font> room, and <font color="red">a game room</font> (or <font color="red">play area</font>).</td>
  </tr>
  <tr>
    <td>Downstairs, there's my parents bedroom, the bathrooms and the maintenance.</td>
    <td>Downstairs, <font color="red">there is</font> my parents' bedroom, the bathrooms, and the <font color="red">maintenance room</font>.</td>
  </tr>
  <tr>
    <td>The exit hyptenbar is a high fin- shaped kadden shart, which has a hitch on the top.</td>
    <td>The <font color="red">exit staircase</font> is a high, <font color="red">fin-shaped ladder</font> (or <font color="red">staircase</font>), which has a <font color="red">handrail</font> on the top.</td>
  </tr>
  <tr>
    <td>The control room shares only one part of the wall with the living room, as you can enter the living room from the control room.</td>
    <td>The control room <font color="red">shares a wall</font> with the living room, as you can enter the living room <font color="red">directly</font> from the control room.</td>
  </tr>
  <tr>
    <td>Because of a wall 9.2.</td>
    <td><font color="red">Due to</font> a wall, <font color="red">section 9.2</font> (or <font color="red">a specific wall section</font>).</td>
  </tr>
  <tr>
    <td>The storage and the guest room have the same size, with the only difference being that the storage is filled with crater and loxes and the guest room contains only a small amount of furniture.</td>
    <td>The storage room and the guest room are the <font color="red">same size</font>, with the only difference being that the storage room is filled with <font color="red">crates</font> and <font color="red">locks</font>, and the guest room contains only a <font color="red">small amount</font> of furniture.</td>
  </tr>
  <tr>
    <td>My room is painted aquamarine and has a big table in the center.</td>
    <td>My room is painted <font color="red">aquamarine</font> and has a <font color="red">large</font> table in the <font color="red">center</font>.</td>
  </tr>
  <tr>
    <td>The kitchen, my brother's room at the dining room and the cool oven is important so let's skip there.</td>
    <td>The kitchen, my brother's room, the dining room, and the <font color="red">cooler</font> (or <font color="red">oven</font>) are <font color="red">worth mentioning</font>, so let's <font color="red">focus</font> on those.</td>
  </tr>
  <tr>
    <td>The maintenance room is grey, with lots of control panels all over it.</td>
    <td>The maintenance room is <font color="red">gray</font>, with <font color="red">numerous</font> control panels all over it.</td>
  </tr>
  <tr>
    <td>As you could've guessed this house is inside a submarine.</td>
    <td><font color="green">This sentence could be a interesting twist, but it feels disconnected from the rest of the text. Consider adding more context or clues throughout the email to make this revelation more believable.</font></td>
  </tr>
</table>

<table>
  <tr>
    <th>Criterion</th>
    <th>Possible Score</th>
    <th>Achieved Score</th>
    <th>Justification</th>
  </tr>
  <tr>
    <td>CRITERION_SPELLING</td>
    <td>10</td>
    <td>4</td>
    <td>Many spelling errors throughout the text.</td>
  </tr>
  <tr>
    <td>CRITERION_PUNCTUATION</td>
    <td>10</td>
    <td>6</td>
    <td>Some missing or incorrect punctuation.</td>
  </tr>
  <tr>
    <td>CRITERION_SENTENCE_STRUCTURE</td>
    <td>10</td>
    <td>5</td>
    <td>Some sentences are unclear or grammatically incorrect.</td>
  </tr>
  <tr>
    <td>CRITERION_STYLE</td>
    <td>10</td>
    <td>7</td>
    <td>The text is generally readable, but some sentences are wordy or awkwardly phrased.</td>
  </tr>
  <tr>
    <td>CRITERION_SCOPE</td>
    <td>10</td>
    <td>8</td>
    <td>The text covers a good range of topics, but could be more detailed or descriptive.</td>
  </tr>
  <tr>
    <td>CRITERION_CONTENT</td>
    <td>10</td>
    <td>6</td>
    <td>The text provides some interesting information, but could be more engaging or informative.</td>
  </tr>
  <tr>
    <td>CRITERION_QUESTIONS</td>
    <td>10</td>
    <td>N/A</td>
    <td>No questions to answer in this text.</td>
  </tr>
  <tr>
    <td>Total</td>
    <td>60</td>
    <td>36</td>
    <td></td>
  </tr>
</table>
"""
	},
}