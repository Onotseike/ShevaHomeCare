using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace ShevaHomeCare.Models
{
    public enum ShevaUserType
    {
        Patient, CareGiver
    }

    public class ApplicationUserRoles : IdentityRole
    {
        public ShevaUserType UserType { get; set; }
    }
}
