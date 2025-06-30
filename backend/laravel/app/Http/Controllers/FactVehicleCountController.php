<?php

namespace App\Http\Controllers;

use App\Models\FactVehicleCount;
use App\Http\Resources\FactVehicleCountResource;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;
use Carbon\Carbon;

class FactVehicleCountController extends Controller
{
    public function index()
    {
        $factVehicleCounts = FactVehicleCount::with(['date', 'time', 'location'])->get();

        return FactVehicleCountResource::collection($factVehicleCounts);
    }

    public function filtered(Request $request)
    {
        $query = FactVehicleCount::with(['date', 'time', 'location']);

        if ($request->has('date')) {
            $date = Carbon::parse($request->input('date'));

            if ($request->has('theme')) {
                $theme = $request->input('theme');

                switch ($theme) {
                    case 1: // Tema diário
                        $query->whereHas('date', function ($q) use ($date) {
                            $q->whereDate('full_date', $date->toDateString());
                        });
                        break;

                    case 2: // Tema semanal
                        // Certifique-se de que o início e o fim da semana estão sendo calculados corretamente
                        $startOfWeek = $date->copy()->startOfWeek(); // Início da semana (segunda-feira por padrão)
                        $endOfWeek = $date->copy()->endOfWeek(); // Fim da semana (domingo por padrão)

                        // Ajuste se a semana deve começar no domingo
                        // $startOfWeek = $date->copy()->startOfWeek(Carbon::SUNDAY);
                        // $endOfWeek = $date->copy()->endOfWeek(Carbon::SUNDAY);

                        $query->whereHas('date', function ($q) use ($startOfWeek, $endOfWeek) {
                            $q->whereBetween('full_date', [$startOfWeek->toDateString(), $endOfWeek->toDateString()]);
                        });
                        break;

                    case 3: // Tema mensal
                        $query->whereHas('date', function ($q) use ($date) {
                            $q->whereYear('full_date', $date->year)
                              ->whereMonth('full_date', $date->month);
                        });
                        break;

                    case 4: // Tema anual
                        $query->whereHas('date', function ($q) use ($date) {
                            $q->whereYear('full_date', $date->year);
                        });
                        break;

                    default:
                        return response()->json(['error' => 'Tema inválido'], 400);
                }
            } else {
                // Caso nenhum tema seja fornecido, use o comportamento padrão (diário)
                $query->whereHas('date', function ($q) use ($date) {
                    $q->whereDate('full_date', $date->toDateString());
                });
            }
        }

        if ($request->has('location_id')) {
            $query->where('location_id', $request->input('location_id'));
        }

        if ($request->has('vehicle_type')) {
            $vehicleType = $request->input('vehicle_type');
            if (in_array($vehicleType, ['car', 'motorcycle', 'bike', 'truck', 'bus'])) {
                $query->where($vehicleType, '>', 0);
            }
        }

        return FactVehicleCountResource::collection($query->get());
    }


    public function totalVehicles(Request $request)
    {
        return response()->json([
            'total_vehicle_count' => $this->aggregateData($request, '*')
        ]);
    }

    public function totalCars(Request $request)
    {
        return response()->json([
            'total_car_count' => $this->aggregateData($request, 'car')
        ]);
    }

    public function totalBikes(Request $request)
    {
        return response()->json([
            'total_bike_count' => $this->aggregateData($request, 'bike')
        ]);
    }

    public function totalTrucks(Request $request)
    {
        return response()->json([
            'total_truck_count' => $this->aggregateData($request, 'truck')
        ]);
    }

    public function totalBuses(Request $request)
    {
        return response()->json([
            'total_bus_count' => $this->aggregateData($request, 'bus')
        ]);
    }

    public function totalMotorcycles(Request $request)
    {
        return response()->json([
            'total_motorcycle_count' => $this->aggregateData($request, 'motorcycle')
        ]);
    }

    public function mostMovimented(Request $request)
    {
        $data = $this->aggregateByLocation($request, 'desc');
        return response()->json([
            'most_movimented_stress' => $data
        ]);
    }

    public function lessMovimented(Request $request)
    {
        $data = $this->aggregateByLocation($request, 'asc');
        return response()->json([
            'less_movimented_stress' => $data
        ]);
    }

    private function aggregateData(Request $request, $vehicleType)
    {
        $date = Carbon::parse($request->input('date'));
        $theme = $request->input('theme', 1);
    
        switch ($theme) {
            case 2:
                $start = $date->copy()->startOfWeek();
                $end = $date->copy()->endOfWeek();
                break;
            case 3:
                $start = $date->copy()->startOfMonth();
                $end = $date->copy()->endOfMonth();
                break;
            case 4:
                $start = $date->copy()->startOfYear();
                $end = $date->copy()->endOfYear();
                break;
            default:
                $start = $date->copy()->startOfDay();
                $end = $date->copy()->endOfDay();
                break;
        }
    
        $query = DB::table('warehouse_vehicle_count_db.fact_vehicle_counts as f')
            ->join('warehouse_vehicle_count_db.dim_date as d', 'f.date_id', '=', 'd.date_id')
            ->whereBetween('d.full_date', [$start->toDateString(), $end->toDateString()]);
    
        if ($vehicleType === '*') {
            $total = $query->select(DB::raw('SUM(car + motorcycle + bike + truck + bus) as total'))->value('total');
            return $total ?? 0;
        } else {
            $total = $query->sum($vehicleType);
            return $total ?? 0;
        }
    }
    

    private function aggregateByLocation(Request $request, $order)
    {
        $date = Carbon::parse($request->input('date'));
        $theme = $request->input('theme', 1);

        switch ($theme) {
            case 2:
                $start = $date->copy()->startOfWeek();
                $end = $date->copy()->endOfWeek();
                break;
            case 3:
                $start = $date->copy()->startOfMonth();
                $end = $date->copy()->endOfMonth();
                break;
            case 4:
                $start = $date->copy()->startOfYear();
                $end = $date->copy()->endOfYear();
                break;
            default:
                $start = $date->copy()->startOfDay();
                $end = $date->copy()->endOfDay();
                break;
        }

        $result = DB::table('warehouse_vehicle_count_db.fact_vehicle_counts as f')
            ->join('warehouse_vehicle_count_db.dim_date as d', 'f.date_id', '=', 'd.date_id')
            ->join('warehouse_vehicle_count_db.dim_location as l', 'f.location_id', '=', 'l.location_id')
            ->whereBetween('d.full_date', [$start->toDateString(), $end->toDateString()])
            ->select('l.location as location_name', DB::raw('SUM(car + motorcycle + bike + truck + bus) as total'))
            ->groupBy('l.location')
            ->orderBy('total', $order)
            ->limit(1)
            ->get();

        return $result;
    }
}
