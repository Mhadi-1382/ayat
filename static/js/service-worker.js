
// const CACHE = "ayat-offline";

// importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
// importScripts('https://storage.googleapis.com/workbox-cdn/releases/7.4.0/workbox-sw.js');

// self.addEventListener("message", (event) => {
// 	if (event.data && event.data.type === "SKIP_WAITING") {
// 		self.skipWaiting();
// 	}
// });

// workbox.routing.registerRoute(
// 	new RegExp('/*'),
// 	new workbox.strategies.StaleWhileRevalidate({
// 		cacheName: CACHE
// 	})
// );


importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.5.4/workbox-sw.js');
importScripts("https://js.pusher.com/beams/service-worker.js");

if (workbox) {
  workbox.routing.registerRoute(
    () => true, 
    new workbox.strategies.NetworkFirst({
      cacheName: 'user-data',
      plugins: [
        new workbox.expiration.ExpirationPlugin({
          maxEntries: Infinity,
        }),
      ],
    })
  );
} else {
  console.log('Workbox could not be loaded.');
}
