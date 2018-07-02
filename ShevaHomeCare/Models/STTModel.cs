using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace ShevaHomeCare.Models
{
    // ReSharper disable once InconsistentNaming
    public class STTModel
    {
        public static readonly string FetchTokenUri = "https://westus.api.cognitive.microsoft.com/sts/v1.0";
        // ReSharper disable once InconsistentNaming
        private static readonly string subscriptionKey = "09ae100b29fe4defb6fe7f0519040889";
        private string _token;
        private Timer _accessTokenRenewer;

        //Access token expires every 10 minutes. Renew it every 9 minutes only.
        private const int RefreshTokenDuration = 9;

        public STTModel()
        {
            // this.subscriptionKey = subscriptionKey;
            _token = FetchToken(FetchTokenUri, subscriptionKey).Result;

            // renew the token every specified minutes
            _accessTokenRenewer = new Timer(OnTokenExpiredCallback,
                                           this,
                                           TimeSpan.FromMinutes(RefreshTokenDuration),
                                           TimeSpan.FromMilliseconds(-1));
        }

        public string GetAccessToken()
        {
            return _token;
        }

        private void RenewAccessToken()
        {
            _token = FetchToken(FetchTokenUri, subscriptionKey).Result;
            Console.WriteLine("Renewed token.");
        }

        private void OnTokenExpiredCallback(object stateInfo)
        {
            try
            {
                RenewAccessToken();
            }
            catch (Exception ex)
            {
                // ReSharper disable once FormatStringProblem
                Console.WriteLine("Failed renewing access token. Details: {0} ", ex.Message);
            }
            finally
            {
                try
                {
                    _accessTokenRenewer.Change(TimeSpan.FromMinutes(RefreshTokenDuration), TimeSpan.FromMilliseconds(-1));
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Failed to reschedule the timer to renew access token. Details: {0}", ex.Message);
                }
            }
        }

        // ReSharper disable once ParameterHidesMember
        private async Task<string> FetchToken(string fetchUri, string subscriptionKey)
        {
            using (var client = new HttpClient())
            {
                client.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", subscriptionKey);
                Console.WriteLine(fetchUri);
                UriBuilder uriBuilder = new UriBuilder(fetchUri);
                uriBuilder.Path += "/issueToken";

                var result = await client.PostAsync(uriBuilder.Uri.AbsoluteUri, null);
                //Console.WriteLine("Token Uri: {0}", uriBuilder.Uri.AbsoluteUri);
                return await result.Content.ReadAsStringAsync();
            }
        }
    }
}
