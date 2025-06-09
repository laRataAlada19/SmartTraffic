<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use App\Http\Controllers\SupersetController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\FactVehicleCountController;

/**
 * Location Routes
 */
Route::get('/locations', [LocationController::class, 'index']);
Route::post('/locations', [LocationController::class, 'store']);
Route::get('/locations/{id}', [LocationController::class, 'show']);
Route::patch('/locations/{id}', [LocationController::class, 'update']);
Route::delete('/locations/{id}', [LocationController::class, 'destroy']);

/**
 * Authentication Routes
 */
Route::post('/auth/login', [AuthController::class, 'login']);
Route::middleware(['auth:sanctum'])->group(function () {
    Route::post('/auth/logout', [AuthController::class, 'logout']);
    Route::post('/auth/refreshtoken', [AuthController::class, 'refreshToken']);
});

/**
 * Superset
 */
Route::get('/superset-token', [SupersetController::class, 'getSupersetToken']);

/**
 * User Routes (Authenticated)
 */
Route::middleware(['auth:sanctum'])->group(function () {
    Route::get('/users/me', [UserController::class, 'showMe']);
    Route::get('/users', [UserController::class, 'index']);
    Route::post('/users', [UserController::class, 'store']);
    Route::get('/users/me/table', [UserController::class, 'getUserTables']);
    Route::post('/users/me/add-table', [AuthController::class, 'updateTable']);
});

/**
 * Fact Vehicle Count Routes
 */
Route::prefix('fact-vehicle-counts')->group(function () {
    Route::get('/', [FactVehicleCountController::class, 'index']);

    // Totals by vehicle type
    Route::get('/total', [FactVehicleCountController::class, 'totalVehicles']);
    Route::get('/total/car', [FactVehicleCountController::class, 'totalCars']);
    Route::get('/total/motorcycle', [FactVehicleCountController::class, 'totalMotorcycles']);
    Route::get('/total/bike', [FactVehicleCountController::class, 'totalBikes']);
    Route::get('/total/truck', [FactVehicleCountController::class, 'totalTrucks']);
    Route::get('/total/bus', [FactVehicleCountController::class, 'totalBuses']);

    // Streets
    Route::get('/must-movimented-streets', [FactVehicleCountController::class, 'mostMovimented']);
    Route::get('/less-movimented-streets', [FactVehicleCountController::class, 'lessMovimented']);
});
