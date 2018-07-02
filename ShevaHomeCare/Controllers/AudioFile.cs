using Microsoft.AspNetCore.Http;

namespace ShevaHomeCare.Controllers
{
    public class AudioFile
    {
        public string Title { get; set; }
        public string FileName { get; set; }
        public IFormFile Recording { get; set; }
    }
}