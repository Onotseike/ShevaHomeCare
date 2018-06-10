using Microsoft.AspNetCore.Identity;

namespace ShevaHomeCare.Models
{
    // Add profile data for application users by adding properties to the ApplicationUser class
    public class ApplicationUser : IdentityUser
    {
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string OtherName { get; set; }
        public string Hint { get; set; }
        public string Email { get; set; }
    }
}
