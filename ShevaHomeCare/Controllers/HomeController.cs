using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using ShevaHomeCare.Data;
using ShevaHomeCare.Models;

namespace ShevaHomeCare.Controllers
{
    [Authorize]
    [RequireHttps]
    public class HomeController : Controller
    {
        private readonly IShevaHCRepo _shevaHcRepo;
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly SignInManager<ApplicationUser> _signInManager;
        private readonly RoleManager<ApplicationUserRoles> _roleManager;
        private readonly ILogger _logger;
        private readonly ApplicationDbContext _context;

        public HomeController(UserManager<ApplicationUser> userManager,
            SignInManager<ApplicationUser> signInManager,
            RoleManager<ApplicationUserRoles> roleManager,
            IShevaHCRepo shevaHcRepo, ILoggerFactory loggerFactory, ApplicationDbContext context)
        {
            _userManager = userManager;
            _roleManager = roleManager;
            _signInManager = signInManager;
            _logger = loggerFactory.CreateLogger<AccountController>();
            _shevaHcRepo = shevaHcRepo;
            _context = context;
        }

        public IActionResult Index()
        {
            return View();
        }

        public async Task<IActionResult> DashBoard()
        {
            ViewData["Message"] = "Your Application's Main DashBoard page.";
            var kabanData = _shevaHcRepo.GetAllKabanItems();
            var user = await GetCurrentUserAsync();
            if (_shevaHcRepo.GetUserRole(user) == "Patient")
            {
               // Debug.WriteLine("Fucking hell");
                var userKabanData = kabanData.Where(kData => kData.PatientName == user.FirstName + " " + user.LastName).Select(kData =>kData);
                var kabanItems = userKabanData.ToList();
               
                ViewBag.datasource = kabanItems;
            }
            else if (_shevaHcRepo.GetUserRole(user) == "CareGiver")
            {
                var userKabanData = kabanData.Where(kData => kData.CareGiverName == user.FirstName + " " + user.LastName).Select(kData => kData);
                ViewBag.datasource = userKabanData.ToList();
            }
            else
            {
                ViewBag.datasource = kabanData;
            }

            
            return View();
        }

        public IActionResult CallBoard()
        {
            ViewData["Message"] = "You can make Video or Voice Calls contact page.";

            return View();
        }

        public IActionResult Error()
        {
            return View(new ErrorViewModel {RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier});
        }

        [HttpPost]
        [Route("/Home/AddPatientTodoItem")]
        public IActionResult AddPatientTodoItem(string itemName, string itemType, string kabanItemDescription,
            string createdItemTimeStamp, string patientName, string careGiverName)
        {
            var itemTypee = KabanItemType.Drug;
            if (itemType == KabanItemType.Exercise.ToString())
            {
                itemTypee = KabanItemType.Exercise;
            }
            else if (itemType == KabanItemType.Meal.ToString())
            {
                itemTypee = KabanItemType.Meal;
            }
            else if (itemType == KabanItemType.Miscellenous.ToString())
            {
                itemTypee = KabanItemType.Miscellenous;
            }
            var kabanItem = new KabanItem
            {

                ItemType = itemTypee,
                ItemName = itemName,
                KabanitemDescription = kabanItemDescription,
                CreatedItemTimeStamp = createdItemTimeStamp,
                DoneItemTimeStamp = null,
                PatientName = patientName,
                CareGiverName = careGiverName,
                Status = "Open"
            };

            _shevaHcRepo.AddKabanItem(kabanItem);
            _shevaHcRepo.SaveDataBaseChanges();
            return Json("Kaban Data Item Added");
        }

        [HttpPost]
        [Route("/Home/ModifyKabanItem")]
        public IActionResult ModifyKabanItem([FromBody] KabanCrudParams param)
        {
            var value = param.Value;

            if (param.Action == "insert" || (param.Action == "batch" && (param.Added.Count > 0)))
            {
                if (param.Added != null && param.Added.Count > 0)
                {
                    foreach (var kabanItem in param.Added)
                    {
                        _shevaHcRepo.AddKabanItem(kabanItem);
                    }
                }

                _shevaHcRepo.SaveDataBaseChanges();
                return Json("Kaban Data Item Added");
            }

            if ((param.Action == "remove") || (param.Action == "batch" && (param.Deleted.Count > 0)))
            {
                foreach (var kabanItem in param.Deleted)
                {
                    var oldKabanItem = _shevaHcRepo
                        .GetAllKabanItems().SingleOrDefault(oKi => oKi.KabanItemID == kabanItem.KabanItemID);
                    if (oldKabanItem != null)
                    {
                        _context.KabanItemsData.Remove(oldKabanItem);

                    }
                }

                _shevaHcRepo.SaveDataBaseChanges();
            }

            if (param.Changed != null && param.Changed.Count > 0)
            {
                foreach (var kabanItem in param.Changed)
                {
                    var oldKItem = _shevaHcRepo
                        .GetAllKabanItems().SingleOrDefault(oKItem => oKItem.KabanItemID == kabanItem.KabanItemID);

                    if (oldKItem != null)
                    {
                        KabanItem updateKabanItem = _context.KabanItemsData.Single(k => k.KabanItemID == kabanItem.KabanItemID);

                        updateKabanItem.Status = kabanItem.Status;
                        if (kabanItem.Status == "Done")
                        {
                            updateKabanItem.DoneItemTimeStamp = DateTime.Now.ToString("g");

                        }
                    }
                }
            }

            _shevaHcRepo.SaveDataBaseChanges();
            return Json("Modification Succeeded");

        }

        [HttpPost]
        [Route("/Home/OnDropKabanItem")]
        public IActionResult OnDropKabanItem(string status, int id)
        {
            var oldKItem = _shevaHcRepo.GetAllKabanItems().SingleOrDefault(oKItem => oKItem.KabanItemID == id);
            if (oldKItem != null)
            {
                oldKItem.Status = status;
                if (status == "Close")
                {
                    oldKItem.DoneItemTimeStamp = DateTime.Now.ToString("g");
                    
                }
                _shevaHcRepo.SaveDataBaseChanges();
            }


            return Json("Modification Succeeded");
        }


        private Task<ApplicationUser> GetCurrentUserAsync()
        {
            return _userManager.GetUserAsync(HttpContext.User);
        }

    }
}
