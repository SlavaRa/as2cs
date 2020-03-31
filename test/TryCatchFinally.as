/**
 * Example of comment.
 */
package com.finegamedesign.anagram {

    // This class is empty.
    public class TryCatchFinally {
        public function TryCatchFinally() {
            try {
                var a:Array = [];
                trace(a.length);
            }
            catch (e:ArgumentError) {
                var i:int = 1;
                trace(i);
            }
            catch (e:Error) {
                var u:uint = 0x1;
                trace(u);
            }
            finally {
                var s:String = "";
                trace(s);
            }
        }
    }
}
