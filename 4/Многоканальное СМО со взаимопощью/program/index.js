const lambda = 7;
const mu = 1;

const time = 100000;

// Generates exponentially distributed numbers using param.
const getNextRandom = (param) => -1/param * Math.log(Math.random());

// Helps to map channels over the invoices.
const channelsDistribution = [
	[],	// This element is added just for convenient indexing.
	[ 8 ],
	[ 4, 4 ],
	[ 3, 3, 2 ],
	[ 2, 2, 2, 2 ],
	[ 2, 2, 2, 1, 1 ],
	[ 2, 2, 1, 1, 1, 1 ],
	[ 2, 1, 1, 1, 1, 1, 1 ],
	[ 1, 1, 1, 1, 1, 1, 1, 1 ],
];

const EventType = {
	Created: 'created',
	Processed: 'processed',
};

let events = [
	// Initialize events with first created invoice.
	{
		type: EventType.Created,
		time: getNextRandom(lambda),
	},
];

let invoices = [];

const getNearestEvent = (events) => {
	let min = Infinity;
	let index = -1;
	
	events.forEach((event, i) => {
		if (event.time < min) {
			min = event.time;
			index = i;
		}
	});
	
	return events[index];
};

const updateEvents = (choosenEvent) => {
	// Remove choosen event.
	events = events.filter((event) => event !== choosenEvent);
	// And change time of all remain events.
	events.forEach((event) => {
		event.time -= choosenEvent.time;
	});
}

let currentTime = 0;
let states = [ 
	0, // S0
	0, // S1
	0, // S2
	0, // S3
	0, // S4
	0, // S5
	0, // S6
	0, // S7
	0, // S8
];

let processed = 0;
let total = 0;

while (currentTime < time) {
	const nearestEvent = getNearestEvent(events);
	updateEvents(nearestEvent);

	currentTime += nearestEvent.time;

	states[invoices.length] += nearestEvent.time;
	
	switch (nearestEvent.type) {
		case EventType.Created: {
			total += 1;

			const invoiceChannelMap = channelsDistribution[invoices.length + 1];
			
			// Don't forget to add event on creation of the next invoice.
			events.push({
				type: EventType.Created,
				time: getNextRandom(lambda),
			});

			if (!invoiceChannelMap) {
				// All channels are processing invoices.
				break;
			}
			
			// Redistribute channels.
			invoices.forEach((invoice, index) => {
				const {
					event,
					channels,
				} = invoice;
				const newChannelsCount = invoiceChannelMap[index];
				
				// Reverse proportion, because more channels is better:
				// 0.3s -- 8channels
				// x    -- 4channels
				// -----------------
				// current event time -- channels
				// new event time     -- new channels count
				// -----------------
				// x = 0.3s * 8/4 = 0.6s
				event.time *= channels/newChannelsCount;
				invoice.channels = newChannelsCount;
			});

			// Get channels count for new invoice.
			const channels = invoiceChannelMap[invoiceChannelMap.length - 1];
			
			// Add new event.
			const event = {
				type: EventType.Processed,
				time: getNextRandom(channels * mu),
			};
			events.push(event);
			
			
			// Add new invoice.
			const invoice = {
				event,
				channels,
			};
			invoices.push(invoice);
			
			// Also store reference to invoice to be able to easily remove it from invoices array when needed.
			event.invoice = invoice;
			
			break;
		}
		case EventType.Processed: {
			processed += 1;

			const { invoice } = nearestEvent;

			// Remove processed invoice from invoices array.
			invoices = invoices.filter((i) => i !== invoice);
			
			const invoiceChannelMap = channelsDistribution[invoices.length];
			
			// Redistribute channels.
			invoices.forEach((invoice, index) => {
				const {
					event,
					channels,
				} = invoice;
				const newChannelsCount = invoiceChannelMap[index];
				
				// Reverse proportion, because more channels is better:
				// 0.3s -- 8channels
				// x    -- 4channels
				// -----------------
				// current event time -- channels
				// new event time     -- new channels count
				// -----------------
				// x = 0.3s * 8/4 = 0.6s
				event.time *= channels/newChannelsCount;
				invoice.channels = newChannelsCount;
			});
			
			break;
		}
	}
}

// Normalize values using currentTime, because currentTime a little bit bigger than time.
states = states.map((state) => state / currentTime);

console.log(states);
console.log('Q: ', processed / total);
console.log('A: ', processed / currentTime);
