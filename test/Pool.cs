using System.Collections;
using System.Collections.Generic;
using /*<com>*/Finegamedesign.Utils/*<DataUtil>*/;
namespace Monster
{
    public class Pool
    {
        public int index;
        private ArrayList pool = new ArrayList(){};
        private int max;
        public delegate var FactoryDelegate1(var factoryArgument);
        public static Dictionary<string, object> Construct(/*<Function>*/FactoryDelegate1 factory, Dictionary<string, object> classNameCounts)
        {
            Dictionary<string, object> pools = new Dictionary<string, object>(){};
            foreach(KeyValuePair<string, object> _entry in classNameCounts){string className = _entry.Key;
                int count = classNameCounts[className];
                Pool pool = new Pool(count, factory, className);
                pools[className] = pool;}
            return pools;
        }
        public Pool(int count, /*<Function>*/FactoryDelegate1 factory, var factoryArgument=null)
        {
            max = count;
            for (int i = 0; i < max; i++)
            {
                var instance;
                if (!object.ReferenceEquals(null, factoryArgument))
                {
                    instance = factory(factoryArgument);
                }
                else
                {
                    instance = factory();
                }
                pool.Add(instance);
            }
            index = 0;
        }
        public var Next()
        {
            var item = pool[index];
            index++;
            if (DataUtil.Length(pool) <= index)
            {
                index = 0;
            }
            return item;
        }
    }
}