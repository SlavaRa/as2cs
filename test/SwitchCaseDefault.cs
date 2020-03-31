using UnityEngine;
using System.Collections;
/**
 * Example of comment.
 */
namespace /*<com>*/Finegamedesign.Anagram {
// This class is empty.
public class SwitchCaseDefault {
    public SwitchCaseDefault() {
        switch (value) {
            case true:
            try {
                ArrayList a = new ArrayList(){};
                Debug.Log(a.Count);
            }
            catch (Exception) {
                int i = 1;
                Debug.Log(i);
            }
            catch (Exception) {
                uint u = 0x1;
                Debug.Log(u);
            }
            finally {
                string s = "";
                Debug.Log(s);
            }
            break;
            default:
            bool result = value;
            return result;
        }
    }
}
}