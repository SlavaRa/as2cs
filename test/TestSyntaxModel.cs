using UnityEngine;
using System.Collections.Generic;
using /*<com>*/Finegamedesign.Utils/*<Model>*/;
namespace /*<com>*/Finegamedesign.Anagram.TestSyntax
{
    public class TestSyntaxModel
    {
        private static void Shuffle(List<string> cards)
        {
            for (int i = DataUtil.Length(cards) - 1; 1 <= i; i--)
            {
                int r = (int)(Mathf.Floor((Random.value % 1.0f) * (i + 1)));
                string swap = cards[r];
                cards[r] = cards[i];
                cards[i] = swap;
            }
        }
        internal string helpState;
        internal int letterMax = 10;
        internal List<string> inputs = new List<string>();
        /**
         * From letter graphic.
         */
        internal float letterWidth = 42.0f;
        internal delegate /*<var>*/void ActionDelegate();
        internal /*<Function>*/ActionDelegate onComplete;
        internal delegate bool IsJustPressed(string letter);
        internal string help;
        internal List<string> outputs = new List<string>();
        internal List<string> completes = new List<string>();
        internal string text;
        internal List<string> word;
        internal float wordPosition = 0.0f;
        internal float wordPositionScaled = 0.0f;
        internal int points = 0;
        internal int score = 0;
        internal string state;
        internal TestSyntaxLevels levels = new TestSyntaxLevels();
        private List<string> available;
        private Dictionary<string, object> repeat = new Dictionary<string, object>(){};
        private List<string> selects;
        private Dictionary<string, object> wordHash;
        private bool isVerbose = false;
        public TestSyntaxModel()
        {
            wordHash = new Dictionary<string, object>(){{"aa", true}};
            Trial(levels.GetParams());
        }
        internal void Trial(Dictionary<string, object> parameters)
        {
            wordPosition = 0.0f;
            help = "";
            wordWidthPerSecond = -0.01f;
            if (parameters.ContainsKey("text")) {
                text = (string)(parameters["text"]);
            }
            if (parameters.ContainsKey("help")) {
                help = (string)(parameters["help"]);
            }
            if (parameters.ContainsKey("wordWidthPerSecond")) {
                wordWidthPerSecond = (float)(parameters["wordWidthPerSecond"]);
            }
            if (parameters.ContainsKey("wordPosition")) {
                wordPosition = (float)(parameters["wordPosition"]);
            }
            available = DataUtil.Split(text, "");
            word = DataUtil.CloneList(available);
            if ("" == help)
            {
                Shuffle(word);
                wordWidthPerSecond = // -0.05;
                // -0.02;
                // -0.01;
                // -0.005;
                -0.002f;
                // -0.001;
                float power =
                // 1.5;
                // 1.75;
                2.0f;
                int baseRate = Mathf.Max(1, letterMax - DataUtil.Length(text));
                wordWidthPerSecond *= Mathf.Pow(baseRate, power);
            }
            selects = DataUtil.CloneList(word);
            repeat = new Dictionary<string, object>(){};
            if (isVerbose) Debug.Log("Model.trial: word[0]: <" + word[0] + ">");
        }
        private int previous = 0;
        private int now = 0;
        internal void UpdateNow(int cumulativeMilliseconds)
        {
            float deltaSeconds = (now - previous) / 1000.0f;
            Update(deltaSeconds);
            previous = now;
        }
        internal void Update(float deltaSeconds)
        {
            UpdatePosition(deltaSeconds);
        }
        internal float width = 720;
        internal float scale = 1.0f;
        private float wordWidthPerSecond;
        internal void ScaleToScreen(float screenWidth)
        {
            scale = screenWidth / width;
        }
        /**
         * Test case:  2015-03 Use Mac. Rosa Zedek expects to read key to change level.
         */
        private void ClampWordPosition()
        {
            float wordWidth = 160;
            float min = wordWidth - width;
            if (wordPosition <= min)
            {
                help = "GAME OVER! TO SKIP ANY WORD, PRESS THE PAGEUP KEY (MAC: FN+UP).  TO GO BACK A WORD, PRESS THE PAGEDOWN KEY (MAC: FN+DOWN).";
                helpState = "gameOver";
            }
            wordPosition = Mathf.Max(min, Mathf.Min(0, wordPosition));
        }
        private void UpdatePosition(float seconds)
        {
            wordPosition += (seconds * width * wordWidthPerSecond);
            ClampWordPosition();
            wordPositionScaled = wordPosition * scale;
            if (isVerbose) Debug.Log("Model.updatePosition: " + wordPosition);
        }
        private float outputKnockback = 0.0f;
        internal bool MayKnockback()
        {
            return 0 < outputKnockback && 1 <= DataUtil.Length(outputs);
        }
        /**
         * Clamp word to appear on screen.  Test case:  2015-04-18 Complete word.  See next word slide in.
         */
        private void PrepareKnockback(int length, bool complete)
        {
            float perLength =
            0.03f;
            // 0.05;
            // 0.1;
            outputKnockback = perLength * width * length;
            if (complete) {
                outputKnockback *= 3;
            }
            ClampWordPosition();
        }
        internal bool OnOutputHitsWord()
        {
            bool enabled = MayKnockback();
            if (enabled)
            {
                wordPosition += outputKnockback;
                Shuffle(word);
                selects = DataUtil.CloneList(word);
                for (int i = 0; i < DataUtil.Length(inputs); i++)
                {
                    string letter = inputs[i];
                    int selected = selects.IndexOf(letter);
                    if (0 <= selected)
                    {
                        selects[selected] = letter.ToLower();
                    }
                }
                outputKnockback = 0;
            }
            return enabled;
        }
        /**
         * @param   justPressed     Filter signature justPressed(letter):Boolean.
         */
        internal List<string> GetPresses(/*<Function>*/IsJustPressed justPressed)
        {
            List<string> presses = new List<string>();
            Dictionary<string, object> letters = new Dictionary<string, object>(){};
            for (int i = 0; i < DataUtil.Length(available); i++)
            {
                string letter = available[i];
                if (letters.ContainsKey(letter))
                {
                    continue;
                }
                else
                {
                    letters[letter] = true;
                }
                if (justPressed(letter))
                {
                    presses.Add(letter);
                }
            }
            return presses;
        }
        /**
         * If letter not available, disable typing it.
         * @return Vector of word indexes.
         */
        internal List<int> Press(List<string> presses)
        {
            Dictionary<string, object> letters = new Dictionary<string, object>(){};
            List<int> selectsNow = new List<int>();
            for (int i = 0; i < DataUtil.Length(presses); i++)
            {
                string letter = presses[i];
                if (letters.ContainsKey(letter))
                {
                    continue;
                }
                else
                {
                    letters[letter] = true;
                }
                int index = available.IndexOf(letter);
                if (0 <= index)
                {
                    available.RemoveRange(index, 1);
                    inputs.Add(letter);
                    int selected = selects.IndexOf(letter);
                    if (0 <= selected)
                    {
                        selectsNow.Add(selected);
                        selects[selected] = letter.ToLower();
                    }
                }
            }
            return selectsNow;
        }
        internal List<int> Backspace()
        {
            List<int> selectsNow = new List<int>();
            if (1 <= DataUtil.Length(inputs))
            {
                string letter = DataUtil.Pop(inputs);
                available.Add(letter);
                int selected = selects.LastIndexOf(letter.ToLower());
                if (0 <= selected)
                {
                    selectsNow.Add(selected);
                    selects[selected] = letter;
                }
            }
            return selectsNow;
        }
        /**
         * @return animation state.
         *      "submit" or "complete":  Word shoots. Test case:  2015-04-18 Anders sees word is a weapon.
         *      "submit":  Shuffle letters.  Test case:  2015-04-18 Jennifer wants to shuffle.  Irregular arrangement of letters.  Jennifer feels uncomfortable.
         * Test case:  2015-04-19 Backspace. Deselect. Submit. Type. Select.
         */
        internal string Submit()
        {
            string submission = DataUtil.Join(inputs, "");
            bool accepted = false;
            state = "wrong";
            if (1 <= DataUtil.Length(submission))
            {
                if (wordHash.ContainsKey(submission))
                {
                    if (repeat.ContainsKey(submission))
                    {
                        state = "repeat";
                        if (levels.index <= 50 && "" == help)
                        {
                            help = "YOU CAN ONLY ENTER EACH SHORTER WORD ONCE.";
                            helpState = "repeat";
                        }
                    }
                    else
                    {
                        if ("repeat" == helpState)
                        {
                            helpState = "";
                            help = "";
                        }
                        repeat[submission] = true;
                        accepted = true;
                        ScoreUp(submission);
                        bool complete = DataUtil.Length(text) == DataUtil.Length(submission);
                        PrepareKnockback(DataUtil.Length(submission), complete);
                        if (complete)
                        {
                            completes = DataUtil.CloneList(word);
                            Trial(levels.Up());
                            state = "complete";
                            if (null != onComplete)
                            {
                                OnComplete();
                            }
                        }
                        else
                        {
                            state = "submit";
                        }
                    }
                }
                outputs = DataUtil.CloneList(inputs);
            }
            if (isVerbose) Debug.Log("Model.submit: " + submission + ". Accepted " + accepted);
            DataUtil.Clear(inputs);
            available = DataUtil.CloneList(word);
            selects = DataUtil.CloneList(word);
            return state;
        }
        private void ScoreUp(string submission)
        {
            points = DataUtil.Length(submission);
            score += points;
        }
        internal void CheatLevelUp(int add)
        {
            score = 0;
            Trial(levels.Up(add));
            wordPosition = 0.0f;
        }
    }
}