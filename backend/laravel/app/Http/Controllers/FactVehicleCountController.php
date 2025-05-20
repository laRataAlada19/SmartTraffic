<?php

namespace App\Http\Controllers;

use App\Models\FactVehicleCount;
use App\Http\Resources\FactVehicleCountResource;

class FactVehicleCountController extends Controller
{
    public function index()
    {
        $factVehicleCounts = FactVehicleCount::with(['date', 'time', 'location'])->get();

        return FactVehicleCountResource::collection($factVehicleCounts);
    }
}
