using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Logging;
using ShevaHomeCare.Data;

namespace ShevaHomeCare.Models
{
    public class ShevaHCRepo : IShevaHCRepo
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<IShevaHCRepo> _logger;

        private readonly UserManager<ApplicationUser> _userManager;
        private readonly RoleManager<ApplicationUserRoles> _roleManager;


        public ShevaHCRepo(ApplicationDbContext context, ILogger<IShevaHCRepo> logger, UserManager<ApplicationUser> userManager, RoleManager<ApplicationUserRoles> roleManager)
        {
            _context = context;
            _logger = logger;

            _userManager = userManager;
            _roleManager = roleManager;
        }


        public IEnumerable<ApplicationUser> GetPatientUsers()
        {
            try
            {

                return _userManager.GetUsersInRoleAsync("Patient").Result;
            }
            catch (Exception ex)
            {
                _logger.LogError("Could not get All Patient Users from database", ex);
                return null;
            }
        }

        public void AddKabanItem(KabanItem kabanItem)
        {
            _context.KabanItemsData.Add(kabanItem);
        }

        public void UpdateKabanItem(KabanItem item)
        {
            _context.KabanItemsData.Update(item);
        }

        public IEnumerable<KabanItem> GetAllKabanItems()
        {
            try
            {
                return _context.KabanItemsData.ToList();
            }
            catch (Exception ex)
            {
                _logger.LogError("Could not get All Kaban Items from database", ex);
                return null;
            }
        }

        public IEnumerable<KabanItem> GetAllKabanItemsForPatient(string username)
        {
            try
            {
                return _context.KabanItemsData.Where(kData => kData.PatientName == username).Select(kData => kData);
            }
            catch (Exception ex)
            {
                _logger.LogError("Could not get Kaban Item Data Associated with Patient from database", ex);
                return null;
            }
        }

        public ApplicationUser GetUser(ClaimsPrincipal usePrincipal)
        {
            try
            {
                return _userManager.GetUserAsync(usePrincipal).Result;
            }
            catch (Exception ex)
            {
                _logger.LogError("Could not User from database", ex);
                return null;
            }
        }

        public string GetUserRole(ApplicationUser user)
        {
            try
            {
                var userRole = _userManager.GetRolesAsync(user).Result.FirstOrDefault();

                return userRole;
            }
            catch (Exception ex)
            {
                _logger.LogError("Could not get Role of User from database", ex);
                return null;
            }
        }

        public bool SaveDataBaseChanges()
        {
            return _context.SaveChanges() > 0;
        }
    }
}
