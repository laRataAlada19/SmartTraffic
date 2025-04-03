<?php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use App\Models\Location;

Route::middleware('api')->group(function () {
    Route::get('/locations', [LocationController::class, 'index']);
    Route::get('/locations/{id}', [LocationController::class, 'show']);
    Route::put('/locations/{id}', [LocationController::class, 'update']);
    Route::delete('/locations/{id}', [LocationController::class, 'destroy']);
});

Route::post('/api/locations', function (Request $request) {
    $validated = $request->validate([
        'location' => 'required|string|max:255',
        'direction' => 'required|string|max:255',
    ]);

    $location = Location::create([
        'location' => $validated['location'],
        'direction' => $validated['direction'],
    ]);

    return response()->json($location, 201);
});