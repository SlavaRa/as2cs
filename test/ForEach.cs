using UnityEngine;
/**
 * Example of comment.
 */
namespace /*<com>*/Finegamedesign.Anagram {
// This class is empty.
public class EmptyClass {
    public EmptyClass() {
        foreach(var _entry in new List<int>(){1,2,3,4}){int i = _entry.Key;
            Debug.Log(i);}
        foreach(int i in new List<int>(){1,2,3,4}){
            Debug.Log(i);}
    }
}
}