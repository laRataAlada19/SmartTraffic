<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use Illuminate\Support\Facades\DB;

Route::get('/locations', [LocationController::class, 'index']);
Route::post('/locations', [LocationController::class, 'store']);
