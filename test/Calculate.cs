using System.Collections.Generic;
using /*<com>*/Finegamedesign.Utils/*<DataUtil>*/;
namespace /*<com>*/Finegamedesign.Powerplant
{
    /**
     * @author Ethan Kennerly
     */
    public class Calculate
    {
        /**
         * Multiply cards in stack.  Add stack products.
         * Example @see TestCalculate.as
         */
        public static int Power(List<List<int>> stacks)
        {
            int power = 0;
            for (int s=0; s < DataUtil.Length(stacks); s++) {
                int product = 0;
                for (int c=0; c < DataUtil.Length(stacks[s]); c++) {
                    if (0 == c) {
                        product = stacks[s][c];
                    }
                    else {
                        product *= stacks[s][c];
                    }
                }
                power += product;
            }
            return power;
        }
        /**
         * Multiply cards in stack.  Add stack products.
         * Example @see TestCalculate.as
         */
        public static string Describe(List<List<int>> stacks)
        {
            string description = "";
            int term_count = 0;
            List<string> products = new List<string>();
            List<List<int>> trimmed = Clone(stacks);
            RemoveEmpty(trimmed);
            for (int s=0; s < DataUtil.Length(trimmed); s++) {
                string product = "";
                term_count += DataUtil.Length(trimmed[s]);
                if (2 <= DataUtil.Length(trimmed) && 2 <= DataUtil.Length(trimmed[s])) {
                    product += "(";
                }
                product += DataUtil.Join(trimmed[s], " x ");
                if (2 <= DataUtil.Length(trimmed) && 2 <= DataUtil.Length(trimmed[s])) {
                    product += ")";
                }
                products.Add(product);
            }
            if (2 <= term_count) {
                description += DataUtil.Join(products, " + ")
                + " = " + Power(trimmed).ToString();
            }
            return description;
        }
        private static void RemoveEmpty(List<List<int>> stacks)
        {
            for (int s = DataUtil.Length(stacks) - 1; 0 <= s; s--) {
                if (DataUtil.Length(stacks[s]) <= 0) {
                    stacks.RemoveRange(s, 1);
                }
            }
        }
        /**
         * Select a card from hand that plays on a stack to match contract,
         * or most nearly approaches contract without going over.
         * Example @see TestCalculate.as
         */
        public static List<bool> StacksUnderContract(int value, List<List<int>> stacks, int contract)
        {
            List<bool> stacks_valid = new List<bool>();
            List<List<int>> hypothetical_stacks = Clone(stacks);
            if (DataUtil.Length(hypothetical_stacks) <= 0 || 1 <= DataUtil.Length(
            hypothetical_stacks[DataUtil.Length(hypothetical_stacks) - 1])) {
                hypothetical_stacks.Add(new List<int>());
            }
            for (int s=0; s < DataUtil.Length(hypothetical_stacks); s++) {
                List<int> stack = hypothetical_stacks[s];
                stack.Add(value);
                int hypothetical_power = Power(hypothetical_stacks);
                stacks_valid.Add(hypothetical_power <= contract);
                DataUtil.Pop(hypothetical_stacks[s]);
            }
            return stacks_valid;
        }
        /**
         * Select a card from hand that plays on a stack to match contract,
         * or most nearly approaches contract without going over.
         * Example @see TestCalculate.as
         */
        public static List<int> Select_value_and_stack(List<int> hand, List<List<int>> stacks, int contract)
        {
            List<int> value_and_stack = new List<int>();
            int max = 0;
            List<List<int>> hypothetical_stacks = Clone(stacks);
            hypothetical_stacks.Add(new List<int>());
            for (int h=0; h < DataUtil.Length(hand); h++) {
                for (int s=0; s < DataUtil.Length(hypothetical_stacks); s++) {
                    List<int> stack = hypothetical_stacks[s];
                    stack.Add(hand[h]);
                    int candidate = Power(hypothetical_stacks);
                    if (max < candidate && candidate <= contract) {
                        max = candidate;
                        value_and_stack = new List<int>();
                        value_and_stack.Add(hand[h]);
                        value_and_stack.Add(s);
                    }
                    DataUtil.Pop(hypothetical_stacks[s]);
                }
            }
            return value_and_stack;
        }
        public static List<List<int>> Clone(List<List<int>> stacks)
        {
            List<List<int>> copy = new List<List<int>>();
            for (int s = 0; s < DataUtil.Length(stacks); s++) {
                List<int> stack = stacks[s];
                List<int> copyStack = new List<int>();
                for (int i = 0; i < DataUtil.Length(stack); i++) {
                    copyStack.Add(stack[i]);
                }
                copy.Add(copyStack);
            }
            return copy;
        }
    }
}