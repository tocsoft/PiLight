﻿using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace PiLight.ClientController
{
    public class Client
    {
        private readonly Uri uri;

        public Client(Uri uri)
        {
            this.uri = uri;
        }

        public static async Task<Client> Discover(TimeSpan? timeout = null)
        {
            var usbClientAddress = new Client(new Uri("http://169.254.3.14"));
            if (await usbClientAddress.TestConnection())
            {
                return usbClientAddress;
            }

            timeout = timeout ?? TimeSpan.FromSeconds(30);

            UdpClient client = new UdpClient();

            client.ExclusiveAddressUse = false;
            IPEndPoint localEp = new IPEndPoint(IPAddress.Any, 1234);

            client.Client.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
            client.ExclusiveAddressUse = false;

            client.Client.Bind(localEp);

            IPAddress multicastAddress = IPAddress.Parse("239.255.4.3");

            NetworkInterface[] networkInterfaces = NetworkInterface.GetAllNetworkInterfaces();

            foreach (NetworkInterface networkInterface in networkInterfaces)
            {
                if ((!networkInterface.Supports(NetworkInterfaceComponent.IPv4)) ||
                    (networkInterface.OperationalStatus != OperationalStatus.Up))
                {
                    continue;
                }

                IPInterfaceProperties adapterProperties = networkInterface.GetIPProperties();
                UnicastIPAddressInformationCollection unicastIPAddresses = adapterProperties.UnicastAddresses;
                IPAddress ipAddress = null;

                foreach (UnicastIPAddressInformation unicastIPAddress in unicastIPAddresses)
                {
                    if (unicastIPAddress.Address.AddressFamily != AddressFamily.InterNetwork)
                    {
                        continue;
                    }

                    ipAddress = unicastIPAddress.Address;
                    break;
                }

                if (ipAddress == null)
                {
                    continue;
                }

                client.JoinMulticastGroup(multicastAddress, ipAddress);
            }

            client.Client.ReceiveTimeout = (int)timeout.Value.TotalMilliseconds;
            try
            {
                var result = await client.ReceiveAsync();

                string strData = Encoding.Unicode.GetString(result.Buffer);
                // strData == ip addres

                return new Client(new Uri("http://" + result.RemoteEndPoint.Address.ToString()));
            }
            catch (SocketException ex) when (ex.SocketErrorCode == SocketError.TimedOut)
            {
                return null;
            }
        }

        public async Task<StatusInfo> GetStatus()
        {
            using (var client = new HttpClient() { BaseAddress = this.uri })
            {
                var result = await client.GetAsync($"/");
                result.EnsureSuccessStatusCode();
                var json = await result.Content.ReadAsStringAsync();
                return JsonConvert.DeserializeObject<StatusInfo>(json);
            }
        }
        public async Task TurnOnLight(Lights light, bool flash = false)
        {
            var action = flash ? "flash" : "light";
            using (var client = new HttpClient() { BaseAddress = this.uri })
            {
                await client.GetAsync($"/{action}/{light.ToString().ToLower()}?force=true");
            }
        }

        public async Task TurnOffAllLights()
        {
            using (var client = new HttpClient() { BaseAddress = this.uri })
            {
                var result = await client.GetAsync($"/light/off");
                result.EnsureSuccessStatusCode();
            }
        }
        public async Task Unpause()
        {
            using (var client = new HttpClient() { BaseAddress = this.uri })
            {
                var result = await client.GetAsync($"/unpause");
                result.EnsureSuccessStatusCode();
            }
        }
        
        private async Task<bool> TestConnection()
        {
            try
            {
                using (var client = new HttpClient() { BaseAddress = this.uri })
                {
                    var result = await client.GetAsync($"/");
                    result.EnsureSuccessStatusCode();
                    return result.StatusCode == HttpStatusCode.OK;
                }
            }
            catch
            {
                return false;
            }
        }
    }
    public enum Lights
    {
        Red,
        Amber,
        Green
    }

    public class StatusInfo
    {
        public bool Amber { get; set; }
        public bool Green { get; set; }
        public bool Red { get; set; }
        public bool Pasued { get; set; }
        public bool Sound { get; set; }
    }
}
