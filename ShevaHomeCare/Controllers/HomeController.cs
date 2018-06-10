using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using ShevaHomeCare.Models;

namespace ShevaHomeCare.Controllers
{
    public class HomeController : Controller
    {
        private readonly IShevaHCRepo _shevaHcRepo;
        private readonly UserManager<ApplicationUser> _userManager;
        private readonly SignInManager<ApplicationUser> _signInManager;
        private readonly RoleManager<ApplicationUserRoles> _roleManager;
        private readonly ILogger _logger;

        public HomeController(UserManager<ApplicationUser> userManager,
            SignInManager<ApplicationUser> signInManager,
            RoleManager<ApplicationUserRoles> roleManager,
            IShevaHCRepo shevaHcRepo, ILoggerFactory loggerFactory)
        {
            _userManager = userManager;
            _roleManager = roleManager;
            _signInManager = signInManager;
            _logger = loggerFactory.CreateLogger<AccountController>();
            _shevaHcRepo = shevaHcRepo;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult DashBoard()
        {
            ViewData["Message"] = "Your Application's Main DashBoard page.";
            var kabanData = _shevaHcRepo.GetAllKabanItems();
            ViewBag.datasource = kabanData;
            return View();
        }

        public IActionResult CallBoard()
        {
            ViewData["Message"] = "Your contact page.";

            return View();
        }

        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
