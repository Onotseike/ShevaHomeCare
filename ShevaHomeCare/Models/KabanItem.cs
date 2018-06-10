﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ShevaHomeCare.Models
{
    public enum KabanItemType
    {
        Meal,Exercise,Drug,Miscellenous
    }

    public class KabanItem
    {

        public string ItemName { get; set; }

        public KabanItemType ItemType { get; set; }

        public string KabanitemDescription { get; set; }

        public string CreatedItemTimeStamp { get; set; }

        public string DoneItemTimeStamp { get; set; }

        public string PatientName { get; set; }

        public string CareGiverName { get; set; }
    }
}
