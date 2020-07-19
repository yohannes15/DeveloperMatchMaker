// // Initiate Muuri Grid
// const grid = new Muuri('.grid');

// // Hold our selected filters
// let filteredProgrammingLanguages = [];
// let filteredDatabaseTypes = [];
// let filteredInterests = []
// let filteredExperiences = []


// // Get All Filterable values
// const programmingLangFilter = document.getElementById('programming-lang-filter');
// const databaseFilter = document.getElementById('database-filter');
// const interestFilter = document.getElementById('interest-filter');
// const experiencesFilter = document.getElementById('experience-filter')
// const allProgrammingLanguages = Array.from(programmingLangFilter.querySelectorAll('option'));
// const allDatabaseTypes = Array.from(databaseFilter.querySelectorAll('option'));
// const allInterests = Array.from(interestFilter.querySelectorAll('option'));
// const allExperiences = Array.from(experiencesFilter.querySelectorAll('option'));

// // Set Defaults
// let selectedProgrammingLanguage = programmingLangFilter.value;
// let selectedDatabaseType = databaseFilter.value;
// let selectedInterest = interestFilter.value;
// let selectedExperience = experiencesFilter.value;


// // Events ------------------------------------------------------
// // filter categories on select
// const selects = document.querySelectorAll('select');
// selects.forEach( item => {
// 	item.addEventListener('change', () => {
// 		filterGrid();
// 	}); 
// });



// // Filter grid ------------------------------------------------
// function filterGrid() {
	
// 	// Get latest select values
// 	selectedProgrammingLanguage = programmingLangFilter.value;
//     selectedDatabaseType = databaseFilter.value;
//     selectedInterest = interestFilter.value;
//     selectedExperience = experiencesFilter.value;
	
// 	// Reset filtered Programming Languages & Database Types
// 	filteredProgrammingLanguages.splice(0,filteredProgrammingLanguages.length);
//     filteredDatabaseTypes.splice(0,filteredDatabaseTypes.length);
//     filteredInterests.splice(0, filteredInterests.length);
//     filteredExperiences.splice(0, filteredExperiences.length);
	
// 	// Programming Languages
// 	if( selectedProgrammingLanguage == 'all' ) {
//         allProgrammingLanguages.forEach( (item) => {
// 			 // exlude the actual 'all' value
// 			( item.value !="all" ? filteredProgrammingLanguages.push(item.value) : '' );
// 		});
// 	} else {
// 		filteredProgrammingLanguages.push(programmingLangFilter.value);
// 	}
// 	console.table(filteredProgrammingLanguages);
	
// 	// Database Types
// 	if( selectedDatabaseType == 'all' ) {
//         allDatabaseTypes.forEach(function(item) {
// 			 // exlude the actual 'all' value
// 			( item.value !="all" ? filteredDatabaseTypes.push(item.value) : '' );
// 		});
// 	} else {
// 		filteredDatabaseTypes.push(databaseFilter.value);
// 	}
//     console.table(filteredDatabaseTypes);
    
//     // Field Interests
//     if( selectedInterest == 'all' ) {
//         allInterests.forEach(function(item) {
// 			 // exlude the actual 'all' value
// 			( item.value !="all" ? filteredInterests.push(item.value) : '' );
// 		});
// 	} else {
// 		filteredInterests.push(interestFilter.value);
// 	}
//     console.table(filteredInterests);

//     // Experience Levels
//     if( selectedInterest == 'all' ) {
//         allExperiences.forEach(function(item) {
// 			 // exlude the actual 'all' value
// 			( item.value !="all" ? filteredExperiences.push(item.value) : '' );
// 		});
// 	} else {
// 		filteredExperiences.push(experiencesFilter.value);
// 	}
//     console.table(filteredExperiences);
    
// 	// Filter the grid
// 	// For each item in the grid array (which corresponds to a gallery item), check if the data-categories and data-types value match any of the values in the select field. If they do, return true
// 	grid.filter( (item) => {
// 		console.log(filteredProgrammingLanguages);
// 		if (
//             filteredProgrammingLanguages.some( (pro) => {
// 					return (item.getElement().dataset.category).indexOf(pro) >= 0;
// 				})
// 			&& // set this to 'or' if you want either option to be true. This way both must be true for the item to display
// 			filteredDatabaseTypes.some( (typ) => {
// 					return (item.getElement().dataset.type).indexOf(typ) >= 0;
// 				})
			
// 		) {
// 			// return items that match both IFs
// 			return true;
// 		}
		
// 	});
// } // end filter grid function



// // Slim Select ---------------
// new SlimSelect({
// 	select: '#programming-lang-filter',
// 	showSearch: false,
// });

// new SlimSelect({
// 	select: '#database-filter',
// 	showSearch: false,
// });

// new SlimSelect({
// 	select: '#interest-filter',
// 	showSearch: false,
// });

// new SlimSelect({
// 	select: '#experience-filter',
// 	showSearch: false,
// });

// // Refresh gallery item dimensions and do muuri refresh after last image has loaded (otherwise delayed loading of image will throw off muuri child element sizing, and items will overlap).
// const galleryImages = document.querySelectorAll('.filp-container');
// let galleryImagesCount = 0;
// galleryImages.forEach( (item) => {
// 	item.addEventListener('load', function () {
//   galleryImagesCount++;
// 		(galleryImagesCount == galleryImages.length ? grid.refreshItems().layout() : '' );
// 	});
// });


// // const galleryImages = document.querySelectorAll('.image-gallery__item img');
// // let galleryImagesCount = 0;
// // galleryImages.forEach( (item) => {
// // 	item.addEventListener('load', function () {
// //   galleryImagesCount++;
// // 		(galleryImagesCount == galleryImages.length ?grid.refreshItems().layout() : '' );
// // 	});
// // });