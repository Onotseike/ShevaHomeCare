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

        void AddKabanItem(KabanItem kabanItem);
        IEnumerable<KabanItem> GetAllKabanItems();

        IEnumerable<KabanItem> GetAllKabanItemsForPatient(string username);


    }
}