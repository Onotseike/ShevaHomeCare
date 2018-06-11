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
