<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use App\Http\Controllers\SupersetController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController; 
use Illuminate\Support\Facades\DB;
use App\Http\Controllers\FactVehicleCountController;
use Illuminate\Container\Attributes\Auth;

Route::get('/locations', [LocationController::class, 'index']);
Route::post('/locations', [LocationController::class, 'store']);
Route::get('/locations/{id}', [LocationController::class, 'show']);
Route::patch('/locations/{id}', [LocationController::class, 'update']);
Route::delete('/locations/{id}', [LocationController::class, 'destroy']);


Route::post('/auth/login', [AuthController::class, 'login']);

Route::get('/superset-token', [SupersetController::class, 'getSupersetToken']);

Route::middleware(['auth:sanctum'])->group(function () {
    Route::post('/auth/logout', [AuthController::class, 'logout']);
    Route::post('/auth/refreshtoken', [AuthController::class, 'refreshToken']);
    Route::get('/users/me', [UserController::class, 'showMe']); // Ensure the UserController class has a 'showMe' method
    Route::get('/users', [UserController::class, 'index']);
    Route::post('/users', [UserController::class, 'store']);
    Route::get('/users/me/table', [UserController::class, 'getUserTables']);
    Route::post('/users/me/add-table', [AuthController::class, 'addTable']);
});


Route::get('/fact-vehicle-counts', [FactVehicleCountController::class, 'index']);
Route::get('/fact-vehicle-counts/total', [FactVehicleCountController::class, 'getTotalVehicleCount']);  
Route::get('/fact-vehicle-counts/total/car', [FactVehicleCountController::class, 'getTotalCarCount']);
Route::get('/fact-vehicle-counts/total/motorcycle', [FactVehicleCountController::class, 'getTotalMotorcycleCount']);
Route::get('/fact-vehicle-counts/total/bike', [FactVehicleCountController::class, 'getTotalBikeCount']);
Route::get('/fact-vehicle-counts/total/truck', [FactVehicleCountController::class, 'getTotalTruckCount']);
Route::get('/fact-vehicle-counts/total/bus', [FactVehicleCountController::class, 'getTotalBusCount']);
Route::get('/fact-vehicle-counts/must-movimented-streets', [FactVehicleCountController::class, 'getMustMovimentedStreets']);
Route::get('/fact-vehicle-counts/less-movimented-streets', [FactVehicleCountController::class, 'getLessMovimentedStreets']);
