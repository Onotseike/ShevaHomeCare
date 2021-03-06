﻿using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using ShevaHomeCare.Data;
using ShevaHomeCare.Models;


namespace ShevaHomeCare.Controllers
{
    [Authorize]
   // [RequireHttps]
    public class HomeController : Controller
    {
        private readonly IShevaHCRepo _shevaHcRepo;
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly SignInManager<ApplicationUser> _signInManager;
        private readonly RoleManager<ApplicationUserRoles> _roleManager;
        private readonly ILogger _logger;
        private readonly ApplicationDbContext _context;
        private readonly IHostingEnvironment _env;

        public HomeController(UserManager<ApplicationUser> userManager,
            SignInManager<ApplicationUser> signInManager,
            RoleManager<ApplicationUserRoles> roleManager,
            IShevaHCRepo shevaHcRepo, ILoggerFactory loggerFactory, ApplicationDbContext context, IHostingEnvironment env)
        {
            _userManager = userManager;
            _roleManager = roleManager;
            _signInManager = signInManager;
            _logger = loggerFactory.CreateLogger<AccountController>();
            _shevaHcRepo = shevaHcRepo;
            _context = context;
            _env = env;
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
                var notDoneKabanItems = kabanItems.Where(kd => kd.Status != "Close").Select(kd => kd).ToList();
                var notDone = kabanItems.Where(kd => kd.Status != "Close").Select(kd => kd).Count();
                ViewData["NotDone"] = notDone;

                ViewData["MealName"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Meal)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["MealDes"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Meal)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();

                ViewData["DrugName"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Drug)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["DrugDes"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Drug)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();

                ViewData["ExerciseName"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Exercise)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["ExerciseDes"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Exercise)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();

                ViewData["MiscName"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Miscellenous)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["MiscDes"] = notDoneKabanItems.Where(kd => kd.ItemType == KabanItemType.Miscellenous)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();




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


        [HttpGet]
        [Route("/Home/QueryKaban")]
        public async Task<IActionResult> QueryKaban(int crud, int item, int number, int ordinal)
        {
            var _activeKabanItems = _shevaHcRepo.GetAllKabanItems();
            var user = await GetCurrentUserAsync();
            var userKabanData = _activeKabanItems.Where(kData => kData.PatientName == user.FirstName + " " + user.LastName).Select(kData => kData);
            var kabanItems = userKabanData.ToList();
            var notDoneKabanItems = kabanItems.Where(kd => kd.Status != "Close").Select(kd => kd).ToList();
            if (item > 3)
            {
                var queryResult = notDoneKabanItems.Skip((ordinal - 1) * number).Take(number);
                var enumerable = queryResult.ToList();
                var dataText = "The results for your query is as follows: ";
                foreach (var kItem in enumerable)
                {
                    dataText += kItem.ItemName + " with a description of: " + kItem.KabanitemDescription;
                }
                return Json(dataText);
            }
            else
            {
                var customeKabanItems = notDoneKabanItems.Where(kd => kd.ItemType.ToString() == Enum.GetName(typeof(KabanItemType),item)).Select(kd => kd).Skip((ordinal - 1) * number).Take(number);
                var enumerable = customeKabanItems.ToList();
                var dataText = "The results for your query is as follows: ";
                foreach (var kItem in enumerable)
                {
                    dataText += kItem.ItemName + " with a description of: " + kItem.KabanitemDescription+". ";
                }
                return Json(dataText);
            }

           
        }

        [HttpPost]
        [Route("/Home/ShevaUpdateKaban")]
        public async Task<IActionResult> ShevaUpdateKaban(int crud, int item, int number, int ordinal, int status)
        {
            var _activeKabanItems = _shevaHcRepo.GetAllKabanItems();
            var user = await GetCurrentUserAsync();
            var userKabanData = _activeKabanItems.Where(kData => kData.PatientName == user.FirstName + " " + user.LastName).Select(kData => kData);
            var kabanItems = userKabanData.ToList();
            var notDoneKabanItems = kabanItems.Where(kd => kd.Status != "Close").Select(kd => kd).ToList();
            if (item > 3)
            {
                var queryResult = notDoneKabanItems.Skip((ordinal - 1) * number).Take(number).ToList();
                Console.WriteLine(queryResult.Count);
                Console.WriteLine(queryResult[0]);
                foreach (var query in queryResult)
                {
                    //query.Status = Enum.GetName(typeof(StatusType), status);
                     var qitem = _shevaHcRepo.GetAllKabanItems().SingleOrDefault(kd => kd.KabanItemID == query.KabanItemID);
                    if (qitem != null) qitem.Status = Enum.GetName(typeof(StatusType), status);
                    //_shevaHcRepo.UpdateKabanItem(query);   
                }

                
            }
            else
            {
                var customeKabanItems = notDoneKabanItems.Where(kd => kd.ItemType.ToString() == Enum.GetName(typeof(KabanItemType), item)).Select(kd => kd).Skip((ordinal - 1) * number).Take(number);
                foreach (var query in customeKabanItems)
                {
                    query.Status = Enum.GetName(typeof(StatusType), status);
                    _shevaHcRepo.UpdateKabanItem(query);
                }

            }
            _shevaHcRepo.SaveDataBaseChanges();
            return Json("Your To-do Items Database has been Updated. Please refresh the page to view changes");


        }



        private Task<ApplicationUser> GetCurrentUserAsync()
        {
            return _userManager.GetUserAsync(HttpContext.User);
        }

    }
}
