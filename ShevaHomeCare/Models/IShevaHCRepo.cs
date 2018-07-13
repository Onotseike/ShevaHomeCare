using System.Collections;
using System.Collections.Generic;
using System.Security.Claims;

namespace ShevaHomeCare.Models
{
    public interface IShevaHCRepo
    {
        bool SaveDataBaseChanges();
        string GetUserRole(ApplicationUser user);
        ApplicationUser GetUser(ClaimsPrincipal userPrincipal);

        IEnumerable<ApplicationUser> GetPatientUsers();

        void AddKabanItem(KabanItem kabanItem);
        void UpdateKabanItem(KabanItem item);
        IEnumerable<KabanItem> GetAllKabanItems();

        IEnumerable<KabanItem> GetAllKabanItemsForPatient(string username);


    }
}