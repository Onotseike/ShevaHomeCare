using System.Collections.Generic;

namespace ShevaHomeCare.Models
{
    public class KabanCrudParams
    {
        public string  Key { get; set; }

        public string  Action { get; set; }

        public List<KabanItem> Added { get; set; }

        public List<KabanItem> Changed { get; set; }

        public List<KabanItem> Deleted { get; set; }

        public KabanItem Value { get; set; }
    }
}
