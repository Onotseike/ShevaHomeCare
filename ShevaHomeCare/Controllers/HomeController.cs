using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
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
    [RequireHttps]
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
                var notDone = kabanItems.Where(kd => kd.Status != "Close").Select(kd => kd).Count();
                ViewData["NotDone"] = notDone;

                ViewData["MealName"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Meal)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["MealDes"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Meal)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();

                ViewData["DrugName"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Drug)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["DrugDes"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Drug)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();

                ViewData["ExerciseName"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Exercise)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["ExerciseDes"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Exercise)
                    .Select(kd => kd.KabanitemDescription).FirstOrDefault();

                ViewData["MiscName"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Miscellenous)
                    .Select(kd => kd.ItemName).FirstOrDefault();
                ViewData["MiscDes"] = kabanItems.Where(kd => kd.ItemType == KabanItemType.Miscellenous)
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



        [HttpPost]
        [Route("/Home/STTAudio")]
        public IActionResult SttAudio()
        {
            var webroot = _env.WebRootPath;
            var extList = new string[] { ".wav" };
           
            string downloadFolder = @"D:\onots\Downloads";

            var files = Directory.GetFiles(downloadFolder , "*.*")
                .Where(n => extList.Contains(System.IO.Path.GetExtension(n), StringComparer.OrdinalIgnoreCase))
                .ToList();
            //Console.WriteLine("GGGG");
            //Console.WriteLine(files.Count);
            string fName = "";
            if (files.Count - 1 != 0)
            {
                fName = String.Concat("audio (", files.Count - 1, ").wav");
            }
            else
            {
                fName = "audio.wav";
            }
               
            //Console.WriteLine(fName);
            string srcFile = Path.Combine(downloadFolder, fName);
            string destFile = Path.Combine(webroot, "audio.wav");
            System.IO.File.Copy(srcFile, destFile, true);


            STTModel sttModel = new STTModel();
            string host = @"speech.platform.bing.com";
            string contentType = @"audio/wav; codec=""audio/pcm""; samplerate=16000";
            string requestUri = "https://westus.api.cognitive.microsoft.com/sts/v1.0";// args[0];

            ///*
            // * Input your own audio file or use read from a microphone stream directly.
            // */
            string audioFile = destFile; //args[1];
            string responseString;
            FileStream fs = null;

            try

            {

                var token = sttModel.GetAccessToken();

                Console.WriteLine("Token: {0}\n", token);

                Console.WriteLine("Request Uri: " + requestUri + Environment.NewLine);



                HttpWebRequest request = null;

                request = (HttpWebRequest)HttpWebRequest.Create(requestUri);

                request.SendChunked = true;

                request.Accept = @"application/json;text/xml";

                request.Method = "POST";

                request.ProtocolVersion = HttpVersion.Version11;

                request.Host = host;

                request.ContentType = contentType;

                request.Headers["Authorization"] = "Bearer " + token;



                using (fs = new FileStream(audioFile, FileMode.Open, FileAccess.Read))

                {



                    /*

                     * Open a request stream and write 1024 byte chunks in the stream one at a time.

                     */

                    byte[] buffer = null;

                    int bytesRead = 0;

                    using (Stream requestStream = request.GetRequestStream())

                    {

                        /*

                         * Read 1024 raw bytes from the input audio file.

                         */

                        buffer = new Byte[checked((uint)Math.Min(1024, (int)fs.Length))];

                        while ((bytesRead = fs.Read(buffer, 0, buffer.Length)) != 0)

                        {

                            requestStream.Write(buffer, 0, bytesRead);

                        }



                        // Flush

                        requestStream.Flush();

                    }



                    /*

                     * Get the response from the service.

                     */

                    Console.WriteLine("Response:");

                    using (WebResponse response = request.GetResponse())

                    {

                        Console.WriteLine(((HttpWebResponse)response).StatusCode);



                        using (StreamReader sr = new StreamReader(response.GetResponseStream() ?? throw new InvalidOperationException()))

                        {

                            responseString = sr.ReadToEnd();

                        }



                        Console.WriteLine(responseString);

                        Console.ReadLine();

                    }

                }

            }

            catch (Exception ex)

            {

                Console.WriteLine(ex.ToString());

                Console.WriteLine(ex.Message);

                Console.ReadLine();

            }

        




            return Json("Done Succeeded");
        }


        private Task<ApplicationUser> GetCurrentUserAsync()
        {
            return _userManager.GetUserAsync(HttpContext.User);
        }

    }
}
